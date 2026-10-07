"""phase3_tables

Revision ID: 4b6c2g76e52d
Revises: 3a5d1fc5d41c
Create Date: 2026-10-07 14:38:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import UUID, JSONB
from pgvector.sqlalchemy import Vector

# revision identifiers, used by Alembic.
revision: str = '4b6c2g76e52d'
down_revision: Union[str, Sequence[str], None] = '3a5d1fc5d41c'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

def upgrade() -> None:
    # Bid Documents
    op.create_table(
        'bid_documents',
        sa.Column('id', UUID(as_uuid=True), primary_key=True),
        sa.Column('bid_id', UUID(as_uuid=True), sa.ForeignKey('bids.id'), nullable=False),
        sa.Column('kind', sa.String(), nullable=False),
        sa.Column('content', sa.String(), nullable=True),
        sa.Column('status', sa.String(), nullable=False, server_default="draft"),
        sa.Column('model', sa.String(), nullable=True),
        sa.Column('prompt_version', sa.String(), nullable=True),
        sa.Column('sources', JSONB(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True),
    )

    # Past Bid Chunks
    op.create_table(
        'past_bid_chunks',
        sa.Column('id', UUID(as_uuid=True), primary_key=True),
        sa.Column('tenant_id', UUID(as_uuid=True), sa.ForeignKey('tenants.id'), nullable=False),
        sa.Column('bid_id', UUID(as_uuid=True), sa.ForeignKey('bids.id'), nullable=False),
        sa.Column('text', sa.String(), nullable=False),
        sa.Column('embedding', Vector(1536), nullable=False),
    )
    
    op.create_index('ix_past_bid_chunks_tenant_id', 'past_bid_chunks', ['tenant_id'])

def downgrade() -> None:
    op.drop_table('past_bid_chunks')
    op.drop_table('bid_documents')
