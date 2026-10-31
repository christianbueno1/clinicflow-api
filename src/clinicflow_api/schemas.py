from datetime import UTC, date, datetime
from typing import Annotated
from uuid import UUID

from pydantic import (
    AwareDatetime,
    BaseModel,
    ConfigDict,
    EmailStr,
    Field,
    StringConstraints,
    field_validator,
)

from clinicflow_api.enums import AppointmentStatus, Sex
from clinicflow_api.validators import validar_cedula_ecuador


class SpecialtyBase(BaseModel):
    name: str = Field(min_length=2, max_length=100)

    @field_validator("name")
    @classmethod
    def strip_name(cls, value: str) -> str:
        return value.strip()


class SpecialtyCreate(SpecialtyBase):
    pass


class SpecialtyUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=2, max_length=100)

    @field_validator("name")
    @classmethod
    def strip_name(cls, value: str | None) -> str | None:
        return value.strip() if value is not None else None


class SpecialtyRead(SpecialtyBase):
    model_config = ConfigDict(from_attributes=True)

    id: UUID


Name = Annotated[
    str, StringConstraints(strip_whitespace=True, min_length=1, max_length=100)
]
LicenseNumber = Annotated[
    str, StringConstraints(strip_whitespace=True, min_length=1, max_length=50)
]


def _check_cedula(value: str | None) -> str | None:
    if value is None:
        return None
    value = value.strip()
    if not validar_cedula_ecuador(value):
        raise ValueError("La cédula ecuatoriana no es válida")
    return value


class DoctorCreate(BaseModel):
    first_name: Name
    last_name: Name
    identification_number: str
    license_number: LicenseNumber
    specialty_id: UUID
    is_active: bool = True

    _validate_cedula = field_validator("identification_number")(_check_cedula)


class DoctorUpdate(BaseModel):
    first_name: Name | None = None
    last_name: Name | None = None
    identification_number: str | None = None
    license_number: LicenseNumber | None = None
    specialty_id: UUID | None = None
    is_active: bool | None = None

    _validate_cedula = field_validator("identification_number")(_check_cedula)


class DoctorRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    first_name: str
    last_name: str
    identification_number: str
    license_number: str
    is_active: bool
    specialty: SpecialtyRead
    created_at: datetime
    updated_at: datetime


Phone = Annotated[
    str, StringConstraints(strip_whitespace=True, pattern=r"^\+?[0-9 ]{7,20}$")
]
Address = Annotated[str, StringConstraints(strip_whitespace=True, max_length=500)]


def _check_birth_date(value: date | None) -> date | None:
    if value is not None and value > datetime.now(UTC).date():
        raise ValueError("La fecha de nacimiento no puede ser futura")
    return value


class PatientCreate(BaseModel):
    first_name: Name
    last_name: Name
    date_of_birth: date
    sex: Sex
    phone: Phone
    identification_number: str
    email: EmailStr | None = None
    address: Address | None = None

    _validate_cedula = field_validator("identification_number")(_check_cedula)
    _validate_birth = field_validator("date_of_birth")(_check_birth_date)


class PatientUpdate(BaseModel):
    first_name: Name | None = None
    last_name: Name | None = None
    date_of_birth: date | None = None
    sex: Sex | None = None
    phone: Phone | None = None
    identification_number: str | None = None
    email: EmailStr | None = None
    address: Address | None = None

    _validate_cedula = field_validator("identification_number")(_check_cedula)
    _validate_birth = field_validator("date_of_birth")(_check_birth_date)


class PatientRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    first_name: str
    last_name: str
    date_of_birth: date
    sex: Sex
    phone: str
    identification_number: str
    email: str | None
    address: str | None
    created_at: datetime
    updated_at: datetime


Reason = Annotated[str, StringConstraints(strip_whitespace=True, max_length=255)]


def _check_future(value: AwareDatetime | None) -> AwareDatetime | None:
    if value is not None and value <= datetime.now(UTC):
        raise ValueError("La cita debe agendarse en el futuro")
    return value


class AppointmentCreate(BaseModel):
    patient_id: UUID
    doctor_id: UUID
    starts_at: AwareDatetime
    duration_minutes: int = Field(default=30, ge=5, le=480)
    reason: Reason | None = None

    _validate_future = field_validator("starts_at")(_check_future)


class AppointmentUpdate(BaseModel):
    """Reprogramar o cambiar el motivo. El estado tiene su propio endpoint."""

    starts_at: AwareDatetime | None = None
    duration_minutes: int | None = Field(default=None, ge=5, le=480)
    reason: Reason | None = None

    _validate_future = field_validator("starts_at")(_check_future)


class AppointmentStatusUpdate(BaseModel):
    status: AppointmentStatus


class AppointmentRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    patient_id: UUID
    doctor_id: UUID
    starts_at: datetime
    ends_at: datetime
    reason: str | None
    status: AppointmentStatus
    created_at: datetime
    updated_at: datetime


class Slot(BaseModel):
    starts_at: datetime
    ends_at: datetime
    available: bool


class AvailabilityRead(BaseModel):
    doctor_id: UUID
    day: date
    timezone: str
    slot_minutes: int
    slots: list[Slot]
