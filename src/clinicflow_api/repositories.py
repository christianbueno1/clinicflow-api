from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from clinicflow_api.models import Specialty


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