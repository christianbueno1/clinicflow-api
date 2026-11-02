from datetime import UTC, datetime
from uuid import UUID

from sqlalchemy import ColumnElement, func, or_, select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from clinicflow_api.enums import AppointmentStatus
from clinicflow_api.exceptions import ConflictError
from clinicflow_api.models import Appointment, Doctor, Patient, Specialty


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

    @staticmethod
    def _conditions(
        specialty_id: UUID | None, is_active: bool | None
    ) -> list[ColumnElement[bool]]:
        conds: list[ColumnElement[bool]] = [Doctor.deleted_at.is_(None)]
        if specialty_id is not None:
            conds.append(Doctor.specialty_id == specialty_id)
        if is_active is not None:
            conds.append(Doctor.is_active == is_active)
        return conds

    async def list_page(
        self,
        *,
        page: int,
        page_size: int,
        specialty_id: UUID | None = None,
        is_active: bool | None = None,
    ) -> tuple[list[Doctor], int]:
        conds = self._conditions(specialty_id, is_active)
        total = (
            await self.session.execute(
                select(func.count()).select_from(Doctor).where(*conds)
            )
        ).scalar_one()
        result = await self.session.execute(
            select(Doctor)
            .options(joinedload(Doctor.specialty))
            .where(*conds)
            .order_by(Doctor.last_name, Doctor.first_name, Doctor.id)  # id desempata
            .offset((page - 1) * page_size)
            .limit(page_size)
        )
        return list(result.scalars()), total


class PatientRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def get(self, patient_id: UUID) -> Patient | None:
        result = await self.session.execute(
            select(Patient).where(
                Patient.id == patient_id, Patient.deleted_at.is_(None)
            )
        )
        return result.scalar_one_or_none()

    # Los unique de la tabla incluyen filas con soft delete, por eso estas
    # dos búsquedas NO filtran deleted_at.
    async def get_by_identification(self, number: str) -> Patient | None:
        result = await self.session.execute(
            select(Patient).where(Patient.identification_number == number)
        )
        return result.scalar_one_or_none()

    async def get_by_email(self, email: str) -> Patient | None:
        result = await self.session.execute(
            select(Patient).where(Patient.email == email)
        )
        return result.scalar_one_or_none()

    async def list(
        self, skip: int = 0, limit: int = 50, q: str | None = None
    ) -> list[Patient]:
        stmt = (
            select(Patient)
            .where(Patient.deleted_at.is_(None))
            .order_by(Patient.last_name, Patient.first_name)
            .offset(skip)
            .limit(limit)
        )
        if q:
            like = f"%{q.strip()}%"
            stmt = stmt.where(
                or_(
                    Patient.first_name.ilike(like),
                    Patient.last_name.ilike(like),
                    Patient.identification_number.ilike(like),
                )
            )
        result = await self.session.execute(stmt)
        return list(result.scalars())

    async def add(self, patient: Patient) -> Patient:
        self.session.add(patient)
        await self.session.commit()
        await self.session.refresh(patient)
        return patient

    async def update(self, patient: Patient) -> Patient:
        await self.session.commit()
        await self.session.refresh(patient)
        return patient

    async def soft_delete(self, patient: Patient) -> None:
        patient.deleted_at = datetime.now(UTC)
        await self.session.commit()

    @staticmethod
    def _conditions(q: str | None) -> list[ColumnElement[bool]]:
        conds: list[ColumnElement[bool]] = [Patient.deleted_at.is_(None)]
        if q and q.strip():
            like = f"%{q.strip()}%"
            conds.append(
                or_(
                    Patient.first_name.ilike(like),
                    Patient.last_name.ilike(like),
                    Patient.identification_number.ilike(like),
                )
            )
        return conds

    async def list_page(
        self, *, page: int, page_size: int, q: str | None = None
    ) -> tuple[list[Patient], int]:
        conds = self._conditions(q)
        total = (
            await self.session.execute(
                select(func.count()).select_from(Patient).where(*conds)
            )
        ).scalar_one()
        result = await self.session.execute(
            select(Patient)
            .where(*conds)
            .order_by(Patient.last_name, Patient.first_name, Patient.id)
            .offset((page - 1) * page_size)
            .limit(page_size)
        )
        return list(result.scalars()), total


class AppointmentRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session

    async def get(self, appointment_id: UUID) -> Appointment | None:
        result = await self.session.execute(
            select(Appointment).where(Appointment.id == appointment_id)
        )
        return result.scalar_one_or_none()

    async def list(
        self,
        skip: int = 0,
        limit: int = 50,
        patient_id: UUID | None = None,
        doctor_id: UUID | None = None,
        status: AppointmentStatus | None = None,
        date_from: datetime | None = None,
        date_to: datetime | None = None,
    ) -> list[Appointment]:
        stmt = (
            select(Appointment)
            .order_by(Appointment.starts_at)
            .offset(skip)
            .limit(limit)
        )
        if patient_id is not None:
            stmt = stmt.where(Appointment.patient_id == patient_id)
        if doctor_id is not None:
            stmt = stmt.where(Appointment.doctor_id == doctor_id)
        if status is not None:
            stmt = stmt.where(Appointment.status == status)
        if date_from is not None:
            stmt = stmt.where(Appointment.starts_at >= date_from)
        if date_to is not None:
            stmt = stmt.where(Appointment.starts_at < date_to)
        result = await self.session.execute(stmt)
        return list(result.scalars())

    async def has_overlap(
        self,
        *,
        starts_at: datetime,
        ends_at: datetime,
        doctor_id: UUID | None = None,
        patient_id: UUID | None = None,
        exclude_id: UUID | None = None,
    ) -> bool:
        stmt = (
            select(Appointment.id)
            .where(
                Appointment.status == AppointmentStatus.SCHEDULED,
                Appointment.starts_at < ends_at,
                Appointment.ends_at > starts_at,
            )
            .limit(1)
        )
        if doctor_id is not None:
            stmt = stmt.where(Appointment.doctor_id == doctor_id)
        if patient_id is not None:
            stmt = stmt.where(Appointment.patient_id == patient_id)
        if exclude_id is not None:
            stmt = stmt.where(Appointment.id != exclude_id)
        return (await self.session.execute(stmt)).first() is not None

    async def has_future_scheduled(
        self, *, patient_id: UUID | None = None, doctor_id: UUID | None = None
    ) -> bool:
        stmt = (
            select(Appointment.id)
            .where(
                Appointment.status == AppointmentStatus.SCHEDULED,
                Appointment.starts_at > datetime.now(UTC),
            )
            .limit(1)
        )
        if patient_id is not None:
            stmt = stmt.where(Appointment.patient_id == patient_id)
        if doctor_id is not None:
            stmt = stmt.where(Appointment.doctor_id == doctor_id)
        return (await self.session.execute(stmt)).first() is not None

    def add(self, appointment: Appointment) -> None:
        self.session.add(appointment)

    async def save(self, appointment: Appointment) -> Appointment:
        try:
            await self.session.commit()
        except IntegrityError as exc:
            await self.session.rollback()
            if getattr(exc.orig, "sqlstate", None) == "23P01":  # exclusion_violation
                raise ConflictError("La cita se solapa con otra existente") from exc
            raise
        await self.session.refresh(appointment)
        return appointment

    async def list_scheduled_between(
        self, doctor_id: UUID, start: datetime, end: datetime
    ) -> list[Appointment]:
        result = await self.session.execute(
            select(Appointment).where(
                Appointment.doctor_id == doctor_id,
                Appointment.status == AppointmentStatus.SCHEDULED,
                Appointment.starts_at < end,
                Appointment.ends_at > start,
            )
        )
        return list(result.scalars())
