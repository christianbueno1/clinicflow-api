from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field, field_validator


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