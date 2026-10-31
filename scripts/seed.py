"""Datos de prueba. Uso: uv run python scripts/seed.py"""

import asyncio

from sqlalchemy import select

from clinicflow_api.database import async_session_factory, engine
from clinicflow_api.models import Doctor, Specialty

SPECIALTIES = ["Cardiología", "Pediatría", "Dermatología", "Medicina General"]

DOCTORS = [
    ("Ana", "Mora", "1710034065", "MSP-0001", "Cardiología"),
    ("Luis", "Paredes", "0912345675", "MSP-0002", "Pediatría"),
    ("Carla", "Vera", "1104680135", "MSP-0003", "Medicina General"),
]


async def seed() -> None:
    async with async_session_factory() as session:
        by_name: dict[str, Specialty] = {}
        for name in SPECIALTIES:
            specialty = (
                await session.execute(select(Specialty).where(Specialty.name == name))
            ).scalar_one_or_none()
            if specialty is None:
                specialty = Specialty(name=name)
                session.add(specialty)
            by_name[name] = specialty
        await session.flush()

        for first, last, cedula, license_number, specialty_name in DOCTORS:
            exists = (
                await session.execute(
                    select(Doctor).where(Doctor.license_number == license_number)
                )
            ).scalar_one_or_none()
            if exists is None:
                session.add(
                    Doctor(
                        first_name=first,
                        last_name=last,
                        identification_number=cedula,
                        license_number=license_number,
                        specialty_id=by_name[specialty_name].id,
                    )
                )
        await session.commit()
    await engine.dispose()
    print("Seed OK")


if __name__ == "__main__":
    asyncio.run(seed())
