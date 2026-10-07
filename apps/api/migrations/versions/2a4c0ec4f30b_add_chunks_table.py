"""add_chunks_table

Revision ID: 2a4c0ec4f30b
Revises: 497587df8861
Create Date: 2026-10-07 10:44:26.067903

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '2a4c0ec4f30b'
down_revision: Union[str, Sequence[str], None] = '497587df8861'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Chunks
    op.create_table(
        'chunks',
        sa.Column('id', sa.UUID(), primary_key=True),
        sa.Column('tender_id', sa.UUID(), sa.ForeignKey('tenders.id'), nullable=False),
        sa.Column('file_key', sa.String(), nullable=False),
        sa.Column('page', sa.Integer(), nullable=True),
        sa.Column('clause', sa.String(), nullable=True),
        sa.Column('text', sa.String(), nullable=False),
        sa.Column('embedding', sa.String(), nullable=True), # Note: using String or custom type for pgvector if not fully supported in pure text alembic output
    )
    # The actual vector type requires 'CREATE EXTENSION vector;' which we added in init_schema.
    # To fully support pgvector in raw alembic, we might just alter column:
    op.execute("ALTER TABLE chunks ALTER COLUMN embedding TYPE vector(1536) USING embedding::vector")

def downgrade() -> None:
    op.drop_table('chunks')
