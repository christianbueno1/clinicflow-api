from enum import StrEnum


class Sex(StrEnum):
    """Sexo del paciente: valores `"male"` y `"female"`."""

    MALE = "male"
    FEMALE = "female"


class AppointmentStatus(StrEnum):
    """Estado de la cita."""

    SCHEDULED = "scheduled"
    COMPLETED = "completed"
    CANCELLED = "cancelled"
    NO_SHOW = "no_show"
