class DomainError(Exception):
    """Base de los errores de negocio."""


class NotFoundError(DomainError):
    pass


class ConflictError(DomainError):
    pass


class SpecialtyAlreadyExistsError(ConflictError):
    """Ya existe una especialidad con el mismo nombre normalizado."""

    def __init__(self, name: str) -> None:
        super().__init__(f"Ya existe una especialidad equivalente a '{name}'")
