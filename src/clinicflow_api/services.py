from datetime import date, datetime, timedelta
from uuid import UUID
from zoneinfo import ZoneInfo

from sqlalchemy.exc import IntegrityError

from clinicflow_api.config import get_settings
from clinicflow_api.enums import AppointmentStatus
from clinicflow_api.models import Appointment, Doctor, Patient, Specialty
from clinicflow_api.repositories import (
    AppointmentRepository,
    DoctorRepository,
    PatientRepository,
    SpecialtyRepository,
)
from clinicflow_api.schemas import (
    AppointmentCreate,
    AppointmentStatusUpdate,
    AppointmentUpdate,
    AvailabilityRead,
    DoctorCreate,
    DoctorUpdate,
    PatientCreate,
    PatientUpdate,
    Slot,
    SpecialtyCreate,
    SpecialtyUpdate,
)

# Campos que admiten null explícito en un PATCH
_PATIENT_NULLABLE = {"email", "address"}


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
        self,
        repo: DoctorRepository,
        specialties: SpecialtyRepository,
        appointments: AppointmentRepository,  # nuevo
    ) -> None:
        self.repo = repo
        self.specialties = specialties
        self.appointments = appointments

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
        if await self.appointments.has_future_scheduled(doctor_id=doctor_id):
            raise ConflictError("El doctor tiene citas programadas")
        await self.repo.soft_delete(doctor)

    async def availability(
        self, doctor_id: UUID, day: date, slot_minutes: int
    ) -> AvailabilityRead:
        doctor = await self.get(doctor_id)
        if not doctor.is_active:
            raise ConflictError("El doctor no está activo")

        cfg = get_settings()
        tz = ZoneInfo(cfg.clinic_timezone)
        open_at = datetime.combine(day, cfg.clinic_open, tzinfo=tz)
        close_at = datetime.combine(day, cfg.clinic_close, tzinfo=tz)
        step = timedelta(minutes=slot_minutes)

        booked = await self.appointments.list_scheduled_between(
            doctor_id, open_at, close_at
        )
        now = datetime.now(tz)

        slots: list[Slot] = []
        cursor = open_at
        while cursor + step <= close_at:
            end = cursor + step
            busy = any(a.starts_at < end and a.ends_at > cursor for a in booked)
            slots.append(
                Slot(starts_at=cursor, ends_at=end, available=not busy and cursor > now)
            )
            cursor = end

        return AvailabilityRead(
            doctor_id=doctor_id,
            day=day,
            timezone=cfg.clinic_timezone,
            slot_minutes=slot_minutes,
            slots=slots,
        )


class PatientService:
    def __init__(
        self, repo: PatientRepository, appointments: AppointmentRepository
    ) -> None:
        self.repo = repo
        self.appointments = appointments

    async def _ensure_unique(self, data: dict, current: Patient | None = None) -> None:
        number = data.get("identification_number")
        if (
            number
            and (current is None or number != current.identification_number)
            and await self.repo.get_by_identification(number)
        ):
            raise ConflictError("Ya existe un paciente con esa cédula")

        email = data.get("email")
        if email:
            email = email.strip().lower()
            if (
                current is None or email != current.email
            ) and await self.repo.get_by_email(email):
                raise ConflictError("Ya existe un paciente con ese email")

    async def create(self, data: PatientCreate) -> Patient:
        payload = data.model_dump()
        await self._ensure_unique(payload)
        return await self.repo.add(Patient(**payload))

    async def get(self, patient_id: UUID) -> Patient:
        patient = await self.repo.get(patient_id)
        if patient is None:
            raise NotFoundError("Paciente no encontrado")
        return patient

    async def list(self, **filters) -> list[Patient]:
        return await self.repo.list(**filters)

    async def update(self, patient_id: UUID, data: PatientUpdate) -> Patient:
        patient = await self.get(patient_id)
        changes = {
            k: v
            for k, v in data.model_dump(exclude_unset=True).items()
            if v is not None or k in _PATIENT_NULLABLE
        }
        await self._ensure_unique(changes, current=patient)
        for field, value in changes.items():
            setattr(patient, field, value)
        return await self.repo.update(patient)

    async def delete(self, patient_id: UUID) -> None:
        patient = await self.get(patient_id)
        if await self.appointments.has_future_scheduled(patient_id=patient_id):
            raise ConflictError("El paciente tiene citas programadas")
        await self.repo.soft_delete(patient)


_TRANSITIONS: dict[AppointmentStatus, set[AppointmentStatus]] = {
    AppointmentStatus.SCHEDULED: {
        AppointmentStatus.COMPLETED,
        AppointmentStatus.CANCELLED,
        AppointmentStatus.NO_SHOW,
    },
}


class AppointmentService:
    def __init__(
        self,
        repo: AppointmentRepository,
        patients: PatientRepository,
        doctors: DoctorRepository,
    ) -> None:
        self.repo = repo
        self.patients = patients
        self.doctors = doctors

    async def _ensure_free(
        self,
        *,
        starts_at: datetime,
        ends_at: datetime,
        doctor_id: UUID,
        patient_id: UUID,
        exclude_id: UUID | None = None,
    ) -> None:
        if await self.repo.has_overlap(
            starts_at=starts_at,
            ends_at=ends_at,
            doctor_id=doctor_id,
            exclude_id=exclude_id,
        ):
            raise ConflictError("El doctor ya tiene una cita en ese horario")
        if await self.repo.has_overlap(
            starts_at=starts_at,
            ends_at=ends_at,
            patient_id=patient_id,
            exclude_id=exclude_id,
        ):
            raise ConflictError("El paciente ya tiene una cita en ese horario")

    async def create(self, data: AppointmentCreate) -> Appointment:
        if await self.patients.get(data.patient_id) is None:
            raise NotFoundError("Paciente no encontrado")
        doctor = await self.doctors.get(data.doctor_id)
        if doctor is None:
            raise NotFoundError("Doctor no encontrado")
        if not doctor.is_active:
            raise ConflictError("El doctor no está activo")

        ends_at = data.starts_at + timedelta(minutes=data.duration_minutes)
        await self._ensure_free(
            starts_at=data.starts_at,
            ends_at=ends_at,
            doctor_id=data.doctor_id,
            patient_id=data.patient_id,
        )
        appointment = Appointment(
            patient_id=data.patient_id,
            doctor_id=data.doctor_id,
            starts_at=data.starts_at,
            ends_at=ends_at,
            reason=data.reason,
        )
        self.repo.add(appointment)
        return await self.repo.save(appointment)

    async def get(self, appointment_id: UUID) -> Appointment:
        appointment = await self.repo.get(appointment_id)
        if appointment is None:
            raise NotFoundError("Cita no encontrada")
        return appointment

    async def list(self, **filters) -> list[Appointment]:
        return await self.repo.list(**filters)

    async def update(
        self, appointment_id: UUID, data: AppointmentUpdate
    ) -> Appointment:
        appointment = await self.get(appointment_id)
        if appointment.status != AppointmentStatus.SCHEDULED:
            raise ConflictError("Solo se puede modificar una cita programada")

        changes = data.model_dump(exclude_unset=True)
        starts_at = changes.get("starts_at") or appointment.starts_at
        duration = changes.get("duration_minutes") or int(
            (appointment.ends_at - appointment.starts_at).total_seconds() // 60
        )
        ends_at = starts_at + timedelta(minutes=duration)

        if starts_at != appointment.starts_at or ends_at != appointment.ends_at:
            await self._ensure_free(
                starts_at=starts_at,
                ends_at=ends_at,
                doctor_id=appointment.doctor_id,
                patient_id=appointment.patient_id,
                exclude_id=appointment.id,
            )
            appointment.starts_at = starts_at
            appointment.ends_at = ends_at
        if "reason" in changes:
            appointment.reason = changes["reason"]
        return await self.repo.save(appointment)

    async def change_status(
        self, appointment_id: UUID, data: AppointmentStatusUpdate
    ) -> Appointment:
        appointment = await self.get(appointment_id)
        if data.status not in _TRANSITIONS.get(appointment.status, set()):
            raise ConflictError(
                f"No se puede pasar de '{appointment.status}' a '{data.status}'"
            )
        appointment.status = data.status
        return await self.repo.save(appointment)
