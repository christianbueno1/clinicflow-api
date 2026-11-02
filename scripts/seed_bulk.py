"""Datos de volumen (Seattle Grace Mercy West), para probar paginación y filtros.

Uso:
    uv run python scripts/seed_bulk.py --doctors 60 --patients 120 --appointments 80
"""

import argparse
import asyncio
import random
import unicodedata
import zlib
from datetime import date, datetime, time, timedelta, timezone

from seed import get_or_create, make_cedula
from sqlalchemy import select

from clinicflow_api.database import async_session_factory, engine
from clinicflow_api.enums import Sex
from clinicflow_api.models import Appointment, Doctor, Patient, Specialty

ECU = timezone(timedelta(hours=-5))

SPECIALTIES = [
    "Cirugía General",
    "Neurocirugía",
    "Cirugía Cardiotorácica",
    "Pediatría",
    "Ortopedia",
    "Cirugía Plástica",
    "Trauma",
    "Neonatología",
    "Cardiología",
    "Anestesiología",
    "Obstetricia y Ginecología",
    "Urgencias",
]

# (nombre, apellido)
DOCTOR_CAST = [
    ("Meredith", "Grey"),
    ("Derek", "Shepherd"),
    ("Cristina", "Yang"),
    ("Izzie", "Stevens"),
    ("George", "O'Malley"),
    ("Alex", "Karev"),
    ("Miranda", "Bailey"),
    ("Richard", "Webber"),
    ("Preston", "Burke"),
    ("Addison", "Montgomery"),
    ("Mark", "Sloan"),
    ("Callie", "Torres"),
    ("Arizona", "Robbins"),
    ("Owen", "Hunt"),
    ("Lexie", "Grey"),
    ("Teddy", "Altman"),
    ("Jackson", "Avery"),
    ("April", "Kepner"),
    ("Amelia", "Shepherd"),
    ("Maggie", "Pierce"),
    ("Jo", "Wilson"),
    ("Nathan", "Riggs"),
    ("Atticus", "Lincoln"),
    ("Levi", "Schmitt"),
    ("Taryn", "Helm"),
    ("Tom", "Koracick"),
    ("Ben", "Warren"),
    ("Catherine", "Fox"),
    ("Erica", "Hahn"),
    ("Stephanie", "Edwards"),
    ("Reed", "Adamson"),
    ("Heather", "Brooks"),
    ("Kepner", "Avery"),
    ("Winston", "Ndugu"),
    ("Jerrica", "Hayes"),
]

# Pacientes y familiares recurrentes de la serie: (nombre, apellido, sexo)
PATIENT_CAST = [
    ("Denny", "Duquette", Sex.MALE),
    ("Ellis", "Grey", Sex.FEMALE),
    ("Thatcher", "Grey", Sex.MALE),
    ("Zola", "Shepherd", Sex.FEMALE),
    ("Bailey", "Shepherd", Sex.MALE),
    ("Tucker", "Jones", Sex.MALE),
    ("Henry", "Burton", Sex.MALE),
    ("Rebecca", "Pope", Sex.FEMALE),
    ("Charles", "Percy", Sex.MALE),
    ("Susan", "Grey", Sex.FEMALE),
    ("Joe", "Wilson", Sex.MALE),
    ("Hank", "Campbell", Sex.MALE),
    ("Ava", "Hunt", Sex.FEMALE),
    ("Sofia", "Robbins", Sex.FEMALE),
    ("Tuck", "Jones", Sex.MALE),
    ("Nicole", "Herman", Sex.FEMALE),
    ("Lucas", "Adams", Sex.MALE),
    ("Joshua", "Kepner", Sex.MALE),
]

FIRST_POOL = [f for f, _ in DOCTOR_CAST] + [f for f, _, _ in PATIENT_CAST]
LAST_POOL = [ln for _, ln in DOCTOR_CAST] + [ln for _, ln, _ in PATIENT_CAST]
FEMALE_HINT = {
    "Meredith",
    "Cristina",
    "Izzie",
    "Miranda",
    "Addison",
    "Callie",
    "Arizona",
    "Lexie",
    "Teddy",
    "April",
    "Amelia",
    "Maggie",
    "Jo",
    "Taryn",
    "Catherine",
    "Erica",
    "Stephanie",
    "Heather",
    "Jerrica",
    "Ellis",
    "Zola",
    "Rebecca",
    "Susan",
    "Ava",
    "Sofia",
    "Nicole",
}


def doctor_rows(n: int) -> list[tuple]:
    rng = random.Random(7)  # semilla fija: siempre los mismos datos
    rows = []
    for i in range(1, n + 1):
        if i <= len(DOCTOR_CAST):
            first, last = DOCTOR_CAST[i - 1]
        else:
            first, last = rng.choice(FIRST_POOL), rng.choice(LAST_POOL)
        rows.append(
            (
                first,
                last,
                make_cedula(f"172{i:06d}"),
                f"GA-{i:04d}",
                SPECIALTIES[i % len(SPECIALTIES)],
                i % 7 != 0,  # uno de cada siete queda inactivo
            )
        )
    return rows


def patient_rows(n: int) -> list[tuple]:
    rng = random.Random(11)
    rows = []
    for i in range(1, n + 1):
        if i <= len(PATIENT_CAST):
            first, last, sex = PATIENT_CAST[i - 1]
        else:
            first, last = rng.choice(FIRST_POOL), rng.choice(LAST_POOL)
            sex = Sex.FEMALE if first in FEMALE_HINT else Sex.MALE
        birth = date(1940, 1, 1) + timedelta(days=rng.randint(0, 365 * 75))
        email = (
            None
            if i % 4 == 0
            else f"{first}.{last}.{i}@example.com".lower().replace("'", "")
        )
        rows.append(
            (
                first,
                last,
                birth,
                sex,
                f"099{i:07d}",
                make_cedula(f"173{i:06d}"),
                email,
            )
        )
    return rows


def appointment_starts(n: int) -> list[datetime]:
    """Un hueco distinto por cita (16 por día, de lunes a viernes): nunca se solapan."""
    day = datetime.now(ECU).date() + timedelta(days=1)
    starts: list[datetime] = []
    while len(starts) < n:
        if day.weekday() < 5:
            for slot in range(16):  # 08:00 a 15:30, cada 30 min
                moment = datetime.combine(day, time(8, 0), tzinfo=ECU) + timedelta(
                    minutes=30 * slot
                )
                starts.append(moment)
        day += timedelta(days=1)
    return starts[:n]


async def seed(
    n_doctors: int,
    n_patients: int,
    n_appointments: int,
    extra: list[tuple[str, int]],
) -> None:
    async with async_session_factory() as session:
        names = list(dict.fromkeys(SPECIALTIES + [s for s, _ in extra]))
        specialties = {
            name: await get_or_create(session, Specialty, {"name": name})
            for name in names
        }

        doctors: list[Doctor] = []
        for first, last, cedula, lic, spec, active in doctor_rows(
            n_doctors
        ) + extra_doctor_rows(extra):
            doctors.append(
                await get_or_create(
                    session,
                    Doctor,
                    {"license_number": lic},
                    first_name=first,
                    last_name=last,
                    identification_number=cedula,
                    specialty_id=specialties[spec].id,
                    is_active=active,
                )
            )

        patients: list[Patient] = []
        for first, last, birth, sex, phone, cedula, email in patient_rows(n_patients):
            patients.append(
                await get_or_create(
                    session,
                    Patient,
                    {"identification_number": cedula},
                    first_name=first,
                    last_name=last,
                    date_of_birth=birth,
                    sex=sex,
                    phone=phone,
                    email=email,
                )
            )

        active_doctors = [d for d in doctors if d.is_active]
        if n_appointments and active_doctors and patients:
            for k, starts_at in enumerate(appointment_starts(n_appointments)):
                await get_or_create(
                    session,
                    Appointment,
                    {
                        "patient_id": patients[k % len(patients)].id,
                        "doctor_id": active_doctors[k % len(active_doctors)].id,
                        "starts_at": starts_at,
                    },
                    ends_at=starts_at + timedelta(minutes=30),
                    reason="Consulta de seguimiento",
                )

        await session.commit()
        total_d = (await session.execute(select(Doctor.id))).all()
        total_p = (await session.execute(select(Patient.id))).all()
    await engine.dispose()
    print(f"Seed bulk OK: {len(total_d)} doctores y {len(total_p)} pacientes en total")


def _slug(name: str) -> str:
    ascii_name = unicodedata.normalize("NFKD", name).encode("ascii", "ignore").decode()
    return "".join(c for c in ascii_name.upper() if c.isalnum())[:30]


def extra_doctor_rows(specs: list[tuple[str, int]]) -> list[tuple]:
    """Doctores extra por especialidad. Las claves dependen del nombre, no del orden."""
    rows = []
    for spec, count in specs:
        rng = random.Random(f"extra-{spec}")  # nombres estables por especialidad
        h = zlib.crc32(spec.encode()) % 1000
        slug = _slug(spec)
        for i in range(1, count + 1):
            rows.append(
                (
                    rng.choice(FIRST_POOL),
                    rng.choice(LAST_POOL),
                    make_cedula(f"174{h:03d}{i:03d}"),
                    f"GA-X-{slug}-{i:03d}",
                    spec,
                    i % 5 != 0,
                )
            )
    return rows


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--doctors", type=int, default=50)
    parser.add_argument("--patients", type=int, default=100)
    parser.add_argument("--appointments", type=int, default=0)
    parser.add_argument(
        "--extra",
        action="append",
        default=[],
        metavar="ESPECIALIDAD:N",
        help="Doctores extra de una especialidad, p. ej. Urología:25 (repetible)",
    )
    args = parser.parse_args()
    extra = [(n.strip(), int(c)) for n, c in (e.rsplit(":", 1) for e in args.extra)]
    asyncio.run(seed(args.doctors, args.patients, args.appointments, extra))
