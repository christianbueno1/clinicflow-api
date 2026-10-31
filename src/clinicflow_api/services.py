from uuid import UUID

from sqlalchemy.exc import IntegrityError

from clinicflow_api.models import Doctor, Specialty
from clinicflow_api.repositories import DoctorRepository, SpecialtyRepository
from clinicflow_api.schemas import (
    DoctorCreate,
    DoctorUpdate,
    SpecialtyCreate,
    SpecialtyUpdate,
)


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
        # SpecialtyService.update
        if (
            "name" in changes
            and changes["name"] != specialty.name
            and await self.repo.get_by_name(changes["name"])
        ):
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


class DoctorService:
    def __init__(
        self, repo: DoctorRepository, specialties: SpecialtyRepository
    ) -> None:
        self.repo = repo
        self.specialties = specialties

    async def _ensure_specialty(self, specialty_id: UUID) -> None:
        if await self.specialties.get(specialty_id) is None:
            raise NotFoundError("Especialidad no encontrada")

    async def _ensure_unique(self, data: dict, current: Doctor | None = None) -> None:
        # DoctorService._ensure_unique
        number = data.get("identification_number")
        if (
            number
            and (current is None or number != current.identification_number)
            and await self.repo.get_by_identification(number)
        ):
            raise ConflictError("Ya existe un doctor con esa cédula")

        license_number = data.get("license_number")
        if (
            license_number
            and (current is None or license_number != current.license_number)
            and await self.repo.get_by_license(license_number)
        ):
            raise ConflictError("Ya existe un doctor con ese número de licencia")

    async def create(self, data: DoctorCreate) -> Doctor:
        await self._ensure_specialty(data.specialty_id)
        payload = data.model_dump()
        await self._ensure_unique(payload)
        return await self.repo.add(Doctor(**payload))

    async def get(self, doctor_id: UUID) -> Doctor:
        doctor = await self.repo.get(doctor_id)
        if doctor is None:
            raise NotFoundError("Doctor no encontrado")
        return doctor

    async def list(self, **filters) -> list[Doctor]:
        return await self.repo.list(**filters)

    async def update(self, doctor_id: UUID, data: DoctorUpdate) -> Doctor:
        doctor = await self.get(doctor_id)
        # Ningún campo del doctor es nullable: ignora los null explícitos
        changes = {
            k: v
            for k, v in data.model_dump(exclude_unset=True).items()
            if v is not None
        }
        if "specialty_id" in changes:
            await self._ensure_specialty(changes["specialty_id"])
        await self._ensure_unique(changes, current=doctor)
        for field, value in changes.items():
            setattr(doctor, field, value)
        return await self.repo.update(doctor)

    async def delete(self, doctor_id: UUID) -> None:
        doctor = await self.get(doctor_id)
        await self.repo.soft_delete(doctor)
