from datetime import datetime
from typing import Annotated
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field, StringConstraints, field_validator

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
