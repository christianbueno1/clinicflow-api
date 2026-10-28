from datetime import date, datetime
from enum import StrEnum
from uuid import UUID, uuid4

from sqlalchemy import Date, DateTime, Enum, String, Text, Uuid, func
from sqlalchemy.orm import Mapped, mapped_column, validates

from clinicflow_api.models.base import Base
from clinicflow_api.validators import validar_cedula_ecuador


class Sex(StrEnum):
    """Sexo del paciente: valores `"male"` y `"female"`."""

    MALE = "male"
    FEMALE = "female"


class Patient(Base):
    __tablename__ = "patients"

    id: Mapped[UUID] = mapped_column(
        Uuid(as_uuid=True),
        primary_key=True,
        default=uuid4,
    )

    first_name: Mapped[str] = mapped_column(String(100), nullable=False)
    last_name: Mapped[str] = mapped_column(String(100), nullable=False)
    date_of_birth: Mapped[date] = mapped_column(Date, nullable=False)
    sex: Mapped[Sex] = mapped_column(
        Enum(
            Sex,
            name="sex",
            native_enum=False,
            create_constraint=True,
            length=6,
            values_callable=lambda enum_cls: [member.value for member in enum_cls],
        ),
        nullable=False,
    )
    phone: Mapped[str] = mapped_column(String(30), nullable=False)

    identification_number: Mapped[str] = mapped_column(
        String(10),
        unique=True,
        nullable=False,
    )

    email: Mapped[str | None] = mapped_column(
        String(254),
        unique=True,
        nullable=True,
    )

    address: Mapped[str | None] = mapped_column(Text, nullable=True)

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False,
    )

    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )

    deleted_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True),
        nullable=True,
        default=None,
    )

    @validates("first_name", "last_name", "phone")
    def normalize_text(self, key: str, value: str) -> str:
        return value.strip()

    @validates("identification_number")
    def normalize_identification_number(
        self,
        key: str,
        value: str,
    ) -> str:
        cedula = value.strip()

        if not validar_cedula_ecuador(cedula):
            raise ValueError("La cédula ecuatoriana no es válida")

        return cedula

    @validates("email")
    def normalize_email(self, key: str, value: str | None) -> str | None:
        if value is None:
            return None

        normalized = value.strip().lower()
        return normalized or None
