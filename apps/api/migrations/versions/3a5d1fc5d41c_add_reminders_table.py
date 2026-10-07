"""add_reminders_table

Revision ID: 3a5d1fc5d41c
Revises: 2a4c0ec4f30b
Create Date: 2026-10-07 14:31:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import UUID

# revision identifiers, used by Alembic.
revision: str = '3a5d1fc5d41c'
down_revision: Union[str, Sequence[str], None] = '2a4c0ec4f30b'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

def upgrade() -> None:
    # Reminders
    op.create_table(
        'reminders',
        sa.Column('id', UUID(as_uuid=True), primary_key=True),
        sa.Column('tenant_id', UUID(as_uuid=True), sa.ForeignKey('tenants.id'), nullable=False),
        sa.Column('tender_id', UUID(as_uuid=True), sa.ForeignKey('tenders.id'), nullable=True),
        sa.Column('due_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('channel', sa.String(), nullable=False, server_default="whatsapp"),
        sa.Column('sent_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
    )

def downgrade() -> None:
    op.drop_table('reminders')
