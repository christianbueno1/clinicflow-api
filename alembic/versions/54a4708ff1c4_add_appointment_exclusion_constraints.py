"""add appointment exclusion constraints

Revision ID: 54a4708ff1c4
Revises: f4a1effcdfdf
Create Date: 2026-10-31 16:16:38.530301

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '54a4708ff1c4'
down_revision: Union[str, Sequence[str], None] = 'f4a1effcdfdf'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
