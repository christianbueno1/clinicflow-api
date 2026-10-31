class DomainError(Exception):
    """Base de los errores de negocio."""


class NotFoundError(DomainError):
    pass


class ConflictError(DomainError):
    pass
