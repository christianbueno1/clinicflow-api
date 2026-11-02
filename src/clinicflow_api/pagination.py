import math

from pydantic import BaseModel


class Page[T](BaseModel):
    items: list[T]
    total: int
    page: int
    page_size: int
    total_pages: int


def paginated(items: list, total: int, page: int, page_size: int) -> dict:
    """Arma la respuesta paginada. Con total = 0, total_pages = 0."""
    return {
        "items": items,
        "total": total,
        "page": page,
        "page_size": page_size,
        "total_pages": math.ceil(total / page_size),
    }
