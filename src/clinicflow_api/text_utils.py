"""Utilidades de texto."""

import unicodedata


def normalize_key(value: str) -> str:
    """Forma canónica para comparar nombres: sin tildes, minúsculas, espacios colapsados."""
    base = unicodedata.normalize("NFKD", value)
    without_accents = "".join(c for c in base if not unicodedata.combining(c))
    return " ".join(without_accents.lower().split())
