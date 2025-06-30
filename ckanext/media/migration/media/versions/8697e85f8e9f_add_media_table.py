"""Add media table

Revision ID: 8697e85f8e9f
Revises:
Create Date: 2025-06-21 14:00:07.819807

"""

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


# revision identifiers, used by Alembic.
revision = "8697e85f8e9f"
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "media",
        sa.Column("id", sa.Integer, primary_key=True, unique=True, autoincrement=True),
        sa.Column("title", sa.Text(), nullable=False),
        sa.Column("file", sa.Text(), nullable=False),
        sa.Column("type", sa.String(), nullable=False),
        sa.Column("author", sa.String(), nullable=False),
        sa.Column(
            "created", sa.DateTime(), server_default=sa.func.now(), nullable=False
        ),
        sa.Column(
            "modified", sa.DateTime(), server_default=sa.func.now(), nullable=False
        ),
        sa.Column("extras", postgresql.JSONB(astext_type=sa.Text()), nullable=True),
    )


def downgrade():
    op.drop_table("media")
