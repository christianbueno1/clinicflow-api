from uuid import UUID

from sqlalchemy.exc import IntegrityError

from clinicflow_api.models import Specialty
from clinicflow_api.repositories import SpecialtyRepository
from clinicflow_api.schemas import SpecialtyCreate, SpecialtyUpdate


class NotFoundError(Exception):
    pass


class ConflictError(Exception):
    pass


class SpecialtyService:
    def __init__(self, repo: SpecialtyRepository) -> None:
        self.repo = repo

    async def create(self, data: SpecialtyCreate) -> Specialty:
        if await self.repo.get_by_name(data.name):
            raise ConflictError("Ya existe una especialidad con ese nombre")
        return await self.repo.add(Specialty(**data.model_dump()))

    async def get(self, specialty_id: UUID) -> Specialty:
        specialty = await self.repo.get(specialty_id)
        if specialty is None:
            raise NotFoundError("Especialidad no encontrada")
        return specialty

    async def list(self, skip: int, limit: int) -> list[Specialty]:
        return await self.repo.list(skip, limit)

    async def update(self, specialty_id: UUID, data: SpecialtyUpdate) -> Specialty:
        specialty = await self.get(specialty_id)
        changes = data.model_dump(exclude_unset=True)
        if "name" in changes and changes["name"] != specialty.name:
            if await self.repo.get_by_name(changes["name"]):
                raise ConflictError("Ya existe una especialidad con ese nombre")
        for field, value in changes.items():
            setattr(specialty, field, value)
        return await self.repo.update(specialty)

    async def delete(self, specialty_id: UUID) -> None:
        specialty = await self.get(specialty_id)
        try:
            await self.repo.delete(specialty)
        except IntegrityError as exc:
            raise ConflictError(
                "No se puede eliminar: tiene doctores asociados"
            ) from exc