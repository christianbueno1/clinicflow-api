"""add specialties name_key

Revision ID: 7a17e5287c99
Revises: bca5d911a2c0
Create Date: 2026-11-02 14:54:09.391969

"""
import unicodedata
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '7a17e5287c99'
down_revision: Union[str, Sequence[str], None] = 'bca5d911a2c0'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def _normalize_key(value: str) -> str:
    # Copia deliberada de clinicflow_api.text_utils.normalize_key: una migración
    # no debe depender de código de la app que puede cambiar después.
    base = unicodedata.normalize("NFKD", value)
    without_accents = "".join(c for c in base if not unicodedata.combining(c))
    return " ".join(without_accents.lower().split())


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column(
        "specialties", sa.Column("name_key", sa.String(length=100), nullable=True)
    )

    bind = op.get_bind()
    rows = bind.execute(sa.text("SELECT id, name FROM specialties")).all()

    keys: dict[str, list[str]] = {}
    for _id, name in rows:
        keys.setdefault(_normalize_key(name), []).append(name)
    duplicates = {k: names for k, names in keys.items() if len(names) > 1}
    if duplicates:
        raise RuntimeError(
            "Hay especialidades duplicadas al normalizar; fusiónalas antes de migrar: "
            f"{duplicates}"
        )

    for _id, name in rows:
        bind.execute(
            sa.text("UPDATE specialties SET name_key = :k WHERE id = :id"),
            {"k": _normalize_key(name), "id": _id},
        )

    op.alter_column("specialties", "name_key", nullable=False)
    op.create_unique_constraint("uq_specialties_name_key", "specialties", ["name_key"])


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_constraint("uq_specialties_name_key", "specialties", type_="unique")
    op.drop_column("specialties", "name_key")