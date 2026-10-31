from datetime import UTC, datetime
from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from clinicflow_api.models import Doctor, Specialty


class SpecialtyRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def get(self, specialty_id: UUID) -> Specialty | None:
        return await self.session.get(Specialty, specialty_id)

    async def get_by_name(self, name: str) -> Specialty | None:
        result = await self.session.execute(
            select(Specialty).where(Specialty.name == name)
        )
        return result.scalar_one_or_none()

    async def list(self, skip: int = 0, limit: int = 50) -> list[Specialty]:
        result = await self.session.execute(
            select(Specialty).order_by(Specialty.name).offset(skip).limit(limit)
        )
        return list(result.scalars())

    async def add(self, specialty: Specialty) -> Specialty:
        self.session.add(specialty)
        await self.session.commit()
        await self.session.refresh(specialty)
        return specialty

    async def update(self, specialty: Specialty) -> Specialty:
        await self.session.commit()
        await self.session.refresh(specialty)
        return specialty

    async def delete(self, specialty: Specialty) -> None:
        await self.session.delete(specialty)
        await self.session.commit()


class DoctorRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def get(self, doctor_id: UUID) -> Doctor | None:
        result = await self.session.execute(
            select(Doctor)
            .options(joinedload(Doctor.specialty))
            .where(Doctor.id == doctor_id, Doctor.deleted_at.is_(None))
            .execution_options(populate_existing=True)
        )
        return result.scalar_one_or_none()

    async def get_by_identification(self, number: str) -> Doctor | None:
        result = await self.session.execute(
            select(Doctor).where(Doctor.identification_number == number)
        )
        return result.scalar_one_or_none()

    async def get_by_license(self, license_number: str) -> Doctor | None:
        result = await self.session.execute(
            select(Doctor).where(Doctor.license_number == license_number)
        )
        return result.scalar_one_or_none()

    async def list(
        self,
        skip: int = 0,
        limit: int = 50,
        specialty_id: UUID | None = None,
        is_active: bool | None = None,
    ) -> list[Doctor]:
        stmt = (
            select(Doctor)
            .options(joinedload(Doctor.specialty))
            .where(Doctor.deleted_at.is_(None))
            .order_by(Doctor.last_name, Doctor.first_name)
            .offset(skip)
            .limit(limit)
        )
        if specialty_id is not None:
            stmt = stmt.where(Doctor.specialty_id == specialty_id)
        if is_active is not None:
            stmt = stmt.where(Doctor.is_active == is_active)
        result = await self.session.execute(stmt)
        return list(result.scalars())

    async def add(self, doctor: Doctor) -> Doctor:
        self.session.add(doctor)
        await self.session.commit()
        return await self.get(doctor.id)  # type: ignore[return-value]

    async def update(self, doctor: Doctor) -> Doctor:
        await self.session.commit()
        return await self.get(doctor.id)  # type: ignore[return-value]

    async def soft_delete(self, doctor: Doctor) -> None:
        doctor.deleted_at = datetime.now(UTC)
        await self.session.commit()
