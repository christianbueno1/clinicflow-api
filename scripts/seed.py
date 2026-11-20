"""Datos de prueba (Princeton-Plainsboro). Uso: uv run python scripts/seed.py"""

import asyncio
from datetime import date, datetime, timedelta, timezone

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from clinicflow_api.database import async_session_factory, engine
from clinicflow_api.models import (
    Appointment,
    AppointmentStatus,
    Doctor,
    Patient,
    Sex,
    Specialty,
)
from clinicflow_api.text_utils import normalize_key
from clinicflow_api.validators import validar_cedula_ecuador

ECU = timezone(timedelta(hours=-5))


def make_cedula(base9: str) -> str:
    """Completa 9 dígitos con el verificador (Módulo 10) y valida el resultado."""
    total = 0
    for i, ch in enumerate(base9):
        d = int(ch) * (2 if i % 2 == 0 else 1)
        total += d - 9 if d > 9 else d
    cedula = base9 + str((10 - total % 10) % 10)
    assert validar_cedula_ecuador(cedula), cedula
    return cedula


SPECIALTIES = [
    "Medicina Diagnóstica",
    "Oncología",
    "Endocrinología",
    "Neurología",
    "Cirugía",
    "Inmunología",
    "Medicina Intensiva",
]

# (nombre, apellido, cédula, licencia, especialidad)
DOCTORS = [
    ("Gregory", "House", "1712345675", "PPTH-0001", "Medicina Diagnóstica"),
    ("James", "Wilson", "1801234566", "PPTH-0002", "Oncología"),
    ("Lisa", "Cuddy", "0102030400", "PPTH-0003", "Endocrinología"),
    ("Eric", "Foreman", "1309876546", "PPTH-0004", "Neurología"),
    ("Robert", "Chase", "0701234569", "PPTH-0005", "Cirugía"),
    ("Allison", "Cameron", make_cedula("170000001"), "PPTH-0006", "Inmunología"),
    ("Chris", "Taub", make_cedula("170000002"), "PPTH-0007", "Cirugía"),
    ("Remy", "Hadley", make_cedula("170000003"), "PPTH-0008", "Medicina Diagnóstica"),
    ("Lawrence", "Kutner", make_cedula("170000004"), "PPTH-0009", "Medicina Intensiva"),
]

# (nombre, apellido, nacimiento, sexo, teléfono, cédula, email)
PATIENTS = [
    (
        "Stacy",
        "Warner",
        date(1968, 3, 14),
        Sex.FEMALE,
        "0991000001",
        make_cedula("171001001"),
        "stacy.warner@example.com",
    ),
    (
        "Michael",
        "Tritter",
        date(1965, 7, 2),
        Sex.MALE,
        "0991000002",
        make_cedula("171001002"),
        None,
    ),
    (
        "Amber",
        "Volakis",
        date(1982, 11, 21),
        Sex.FEMALE,
        "0991000003",
        make_cedula("171001003"),
        "amber.v@example.com",
    ),
    (
        "Lucas",
        "Douglas",
        date(1975, 5, 30),
        Sex.MALE,
        "0991000004",
        make_cedula("171001004"),
        None,
    ),
    (
        "Dominika",
        "Petrova",
        date(1990, 1, 9),
        Sex.FEMALE,
        "0991000005",
        make_cedula("171001005"),
        "dominika@example.com",
    ),
]


def at(day: int, hour: int, minute: int = 0) -> datetime:
    """Noviembre 2026, hora de Ecuador."""
    return datetime(2026, 11, day, hour, minute, tzinfo=ECU)


# (cédula paciente, licencia doctor, inicio, motivo, estado)
APPOINTMENTS = [
    (
        PATIENTS[0][5],
        "PPTH-0003",
        at(2, 9),
        "Control de tiroides",
        AppointmentStatus.SCHEDULED,
    ),
    (
        PATIENTS[1][5],
        "PPTH-0004",
        at(2, 10),
        "Dolores de cabeza recurrentes",
        AppointmentStatus.SCHEDULED,
    ),
    (
        PATIENTS[2][5],
        "PPTH-0006",
        at(2, 11),
        "Alergias severas",
        AppointmentStatus.SCHEDULED,
    ),
    (
        PATIENTS[3][5],
        "PPTH-0005",
        at(3, 9),
        "Valoración quirúrgica",
        AppointmentStatus.SCHEDULED,
    ),
    (
        PATIENTS[4][5],
        "PPTH-0008",
        at(3, 10),
        "Síntomas sin diagnóstico",
        AppointmentStatus.SCHEDULED,
    ),
    (
        PATIENTS[0][5],
        "PPTH-0007",
        at(4, 15),
        "Seguimiento postoperatorio",
        AppointmentStatus.CANCELLED,
    ),
    (
        PATIENTS[1][5],
        "PPTH-0009",
        datetime(2026, 10, 28, 8, 0, tzinfo=ECU),
        "Chequeo general",
        AppointmentStatus.COMPLETED,
    ),
]


async def get_or_create(session: AsyncSession, model, lookup: dict, **values):
    """Busca por `lookup` (incluye filas con soft delete); si no existe, la crea."""
    obj = (
        await session.execute(select(model).filter_by(**lookup))
    ).scalar_one_or_none()
    if obj is None:
        obj = model(**lookup, **values)
        session.add(obj)
        await session.flush()
    return obj


async def seed() -> None:
    async with async_session_factory() as session:
        specialties = {
            name: await get_or_create(
                session, Specialty, {"name_key": normalize_key(name)}, name=name
            )
            for name in SPECIALTIES
        }

        doctors: dict[str, Doctor] = {}
        for first, last, cedula, license_number, specialty in DOCTORS:
            doctors[license_number] = await get_or_create(
                session,
                Doctor,
                {"license_number": license_number},
                first_name=first,
                last_name=last,
                identification_number=cedula,
                specialty_id=specialties[specialty].id,
            )

        patients: dict[str, Patient] = {}
        for first, last, birth, sex, phone, cedula, email in PATIENTS:
            patients[cedula] = await get_or_create(
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

        for cedula, license_number, starts_at, reason, status in APPOINTMENTS:
            await get_or_create(
                session,
                Appointment,
                {
                    "patient_id": patients[cedula].id,
                    "doctor_id": doctors[license_number].id,
                    "starts_at": starts_at,
                },
                ends_at=starts_at + timedelta(minutes=30),
                reason=reason,
                status=status,
            )

        await session.commit()
    await engine.dispose()
    print("Seed OK")


if __name__ == "__main__":
    asyncio.run(seed())
