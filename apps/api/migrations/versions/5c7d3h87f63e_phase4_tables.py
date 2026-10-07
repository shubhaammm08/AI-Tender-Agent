"""phase4_tables

Revision ID: 5c7d3h87f63e
Revises: 4b6c2g76e52d
Create Date: 2026-10-07 14:58:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import UUID

# revision identifiers, used by Alembic.
revision: str = '5c7d3h87f63e'
down_revision: Union[str, Sequence[str], None] = '4b6c2g76e52d'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

def upgrade() -> None:
    # Price History
    op.create_table(
        'price_history',
        sa.Column('id', sa.BigInteger(), primary_key=True, autoincrement=True),
        sa.Column('item', sa.String(), nullable=False),
        sa.Column('buyer', sa.String(), nullable=True),
        sa.Column('state', sa.String(), nullable=True),
        sa.Column('l1_price', sa.Numeric(), nullable=True),
        sa.Column('awarded_on', sa.DateTime(timezone=True), nullable=True),
    )

    # User Tenant Access (Consultant Workspace)
    op.create_table(
        'user_tenant_access',
        sa.Column('id', UUID(as_uuid=True), primary_key=True),
        sa.Column('user_id', UUID(as_uuid=True), sa.ForeignKey('users.id'), nullable=False),
        sa.Column('tenant_id', UUID(as_uuid=True), sa.ForeignKey('tenants.id'), nullable=False),
    )
    
    op.create_index('ix_user_tenant_access_user_id', 'user_tenant_access', ['user_id'])

def downgrade() -> None:
    op.drop_table('user_tenant_access')
    op.drop_table('price_history')
