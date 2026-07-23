"""Initial schema placeholder — runtime also uses create_all for local bootstraps."""

from __future__ import annotations

revision = "0001_initial"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Tables are defined on SQLAlchemy metadata; use `alembic revision --autogenerate`
    # for subsequent schema changes. Initial local boot still uses create_all.
    pass


def downgrade() -> None:
    pass
