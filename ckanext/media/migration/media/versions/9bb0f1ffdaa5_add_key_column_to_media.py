"""Add key column to media

Revision ID: 9bb0f1ffdaa5
Revises: 8697e85f8e9f
Create Date: 2025-06-22 00:39:43.397605

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '9bb0f1ffdaa5'
down_revision = '8697e85f8e9f'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column(
        "media",
        sa.Column("key", sa.Text()),
    )


def downgrade():
    op.drop_column("media", "key")
