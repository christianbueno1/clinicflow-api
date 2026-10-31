"""Modelos ORM de ClinicFlow."""

from datetime import date, datetime
from typing import ClassVar
from uuid import UUID, uuid4

from sqlalchemy import (
    CheckConstraint,
    Date,
    DateTime,
    Enum,
    ForeignKey,
    MetaData,
    String,
    Text,
    Uuid,
    func,
    text,
)
from sqlalchemy.dialects.postgresql import ExcludeConstraint
from sqlalchemy.orm import (
    DeclarativeBase,
    Mapped,
    mapped_column,
    relationship,
    validates,
)

from clinicflow_api.enums import AppointmentStatus, Sex
from clinicflow_api.validators import validar_cedula_ecuador

NAMING_CONVENTION = {
    "ix": "ix_%(column_0_label)s",
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s",
}


class Base(DeclarativeBase):
    """Base class for all ORM models."""

    metadata = MetaData(naming_convention=NAMING_CONVENTION)


class TimestampMixin:
    """Columnas de auditoría y soft delete."""

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )
    deleted_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True, default=None
    )


class Specialty(Base):
    __tablename__ = "specialties"

    id: Mapped[UUID] = mapped_column(
        Uuid(as_uuid=True), primary_key=True, default=uuid4
    )
    name: Mapped[str] = mapped_column(String(100), unique=True, nullable=False)

    doctors: Mapped[list["Doctor"]] = relationship(back_populates="specialty")

    @validates("name")
    def normalize_name(self, key: str, value: str) -> str:
        return value.strip()


class Doctor(TimestampMixin, Base):
    __tablename__ = "doctors"

    __mapper_args__: ClassVar[dict] = {"eager_defaults": True}

    id: Mapped[UUID] = mapped_column(
        Uuid(as_uuid=True), primary_key=True, default=uuid4
    )
    first_name: Mapped[str] = mapped_column(String(100), nullable=False)
    last_name: Mapped[str] = mapped_column(String(100), nullable=False)
    identification_number: Mapped[str] = mapped_column(
        String(10), unique=True, nullable=False
    )
    license_number: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    is_active: Mapped[bool] = mapped_column(default=True, nullable=False)

    specialty_id: Mapped[UUID] = mapped_column(
        ForeignKey("specialties.id", ondelete="RESTRICT"), index=True, nullable=False
    )

    specialty: Mapped["Specialty"] = relationship(back_populates="doctors")
    appointments: Mapped[list["Appointment"]] = relationship(back_populates="doctor")

    @validates("first_name", "last_name", "license_number")
    def normalize_text(self, key: str, value: str) -> str:
        return value.strip()

    @validates("identification_number")
    def normalize_identification_number(self, key: str, value: str) -> str:
        cedula = value.strip()
        if not validar_cedula_ecuador(cedula):
            raise ValueError("La cédula ecuatoriana no es válida")
        return cedula


class Patient(TimestampMixin, Base):
    __tablename__ = "patients"

    __mapper_args__: ClassVar[dict] = {"eager_defaults": True}

    id: Mapped[UUID] = mapped_column(
        Uuid(as_uuid=True), primary_key=True, default=uuid4
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
            values_callable=lambda enum_cls: [m.value for m in enum_cls],
        ),
        nullable=False,
    )
    phone: Mapped[str] = mapped_column(String(30), nullable=False)
    identification_number: Mapped[str] = mapped_column(
        String(10), unique=True, nullable=False
    )
    email: Mapped[str | None] = mapped_column(String(254), unique=True, nullable=True)
    address: Mapped[str | None] = mapped_column(Text, nullable=True)

    appointments: Mapped[list["Appointment"]] = relationship(
        back_populates="patient", order_by="Appointment.starts_at"
    )

    @validates("first_name", "last_name", "phone")
    def normalize_text(self, key: str, value: str) -> str:
        return value.strip()

    @validates("identification_number")
    def normalize_identification_number(self, key: str, value: str) -> str:
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


class Appointment(TimestampMixin, Base):
    __tablename__ = "appointments"

    __mapper_args__: ClassVar[dict] = {"eager_defaults": True}
    __table_args__ = (
        CheckConstraint("ends_at > starts_at", name="ends_after_starts"),
        ExcludeConstraint(
            ("doctor_id", "="),
            (func.tstzrange(text("starts_at"), text("ends_at")), "&&"),
            where=text("status = 'scheduled'"),
            using="gist",
            name="ex_appointments_doctor_no_overlap",
        ),
        ExcludeConstraint(
            ("patient_id", "="),
            (func.tstzrange(text("starts_at"), text("ends_at")), "&&"),
            where=text("status = 'scheduled'"),
            using="gist",
            name="ex_appointments_patient_no_overlap",
        ),
    )

    id: Mapped[UUID] = mapped_column(
        Uuid(as_uuid=True), primary_key=True, default=uuid4
    )

    patient_id: Mapped[UUID] = mapped_column(
        ForeignKey("patients.id", ondelete="RESTRICT"), index=True, nullable=False
    )
    doctor_id: Mapped[UUID] = mapped_column(
        ForeignKey("doctors.id", ondelete="RESTRICT"), index=True, nullable=False
    )

    starts_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), index=True, nullable=False
    )
    ends_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    reason: Mapped[str | None] = mapped_column(String(255), nullable=True)
    status: Mapped[AppointmentStatus] = mapped_column(
        Enum(
            AppointmentStatus,
            name="appointment_status",
            native_enum=False,
            create_constraint=True,
            length=9,
            values_callable=lambda enum_cls: [m.value for m in enum_cls],
        ),
        default=AppointmentStatus.SCHEDULED,
        nullable=False,
    )

    patient: Mapped["Patient"] = relationship(back_populates="appointments")
    doctor: Mapped["Doctor"] = relationship(back_populates="appointments")
