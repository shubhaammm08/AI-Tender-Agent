"""init_schema

Revision ID: 497587df8861
Revises: 
Create Date: 2026-10-06 15:22:03.262633

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import UUID, JSONB

# revision identifiers, used by Alembic.
revision: str = '497587df8861'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Extensions
    op.execute("CREATE EXTENSION IF NOT EXISTS vector")

    # Tenants
    op.create_table(
        'tenants',
        sa.Column('id', UUID(as_uuid=True), primary_key=True),
        sa.Column('name', sa.String(), nullable=False),
        sa.Column('plan', sa.String(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True),
    )

    # Users
    op.create_table(
        'users',
        sa.Column('id', UUID(as_uuid=True), primary_key=True),
        sa.Column('tenant_id', UUID(as_uuid=True), sa.ForeignKey('tenants.id'), nullable=False),
        sa.Column('email', sa.String(), nullable=False, unique=True),
        sa.Column('hashed_password', sa.String(), nullable=False),
        sa.Column('role', sa.String(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True),
    )

    # Company Profile
    op.create_table(
        'company_profile',
        sa.Column('id', UUID(as_uuid=True), primary_key=True),
        sa.Column('tenant_id', UUID(as_uuid=True), sa.ForeignKey('tenants.id'), nullable=False, unique=True),
        sa.Column('gstin', sa.String(), nullable=True),
        sa.Column('pan', sa.String(), nullable=True),
        sa.Column('udyam_no', sa.String(), nullable=True),
        sa.Column('turnover', sa.Numeric(), nullable=True),
        sa.Column('categories', JSONB(), nullable=True),
        sa.Column('states', JSONB(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True),
    )

    # Documents
    op.create_table(
        'documents',
        sa.Column('id', UUID(as_uuid=True), primary_key=True),
        sa.Column('tenant_id', UUID(as_uuid=True), sa.ForeignKey('tenants.id'), nullable=False),
        sa.Column('type', sa.String(), nullable=False),
        sa.Column('file_key', sa.String(), nullable=False),
        sa.Column('issued_on', sa.Date(), nullable=True),
        sa.Column('expires_on', sa.Date(), nullable=True),
        sa.Column('version', sa.Integer(), nullable=False, default=1),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=True),
    )
    
    # Enable RLS on Documents
    op.execute("ALTER TABLE documents ENABLE ROW LEVEL SECURITY")
    op.execute("CREATE POLICY tenant_isolation ON documents USING (tenant_id = current_setting('app.tenant_id')::uuid)")

    # Tenders
    op.create_table(
        'tenders',
        sa.Column('id', UUID(as_uuid=True), primary_key=True),
        sa.Column('portal', sa.String(), nullable=False),
        sa.Column('portal_tender_id', sa.String(), nullable=False),
        sa.Column('title', sa.String(), nullable=False),
        sa.Column('buyer', sa.String(), nullable=True),
        sa.Column('state', sa.String(), nullable=True),
        sa.Column('category', sa.String(), nullable=True),
        sa.Column('estimated_value', sa.Numeric(), nullable=True),
        sa.Column('emd', sa.Numeric(), nullable=True),
        sa.Column('closes_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('status', sa.String(), nullable=False, server_default='open'),
        sa.Column('current_version', sa.Integer(), nullable=False, default=1),
        sa.UniqueConstraint('portal', 'portal_tender_id', name='uq_portal_tender_id'),
    )

    # Tender Versions
    op.create_table(
        'tender_versions',
        sa.Column('id', UUID(as_uuid=True), primary_key=True),
        sa.Column('tender_id', UUID(as_uuid=True), sa.ForeignKey('tenders.id'), nullable=False),
        sa.Column('version', sa.Integer(), nullable=False),
        sa.Column('diff', JSONB(), nullable=True),
        sa.Column('fetched_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
    )

    # Tender Files
    op.create_table(
        'tender_files',
        sa.Column('id', UUID(as_uuid=True), primary_key=True),
        sa.Column('tender_id', UUID(as_uuid=True), sa.ForeignKey('tenders.id'), nullable=False),
        sa.Column('kind', sa.String(), nullable=False),
        sa.Column('file_key', sa.String(), nullable=False),
        sa.Column('sha256', sa.String(), nullable=True),
    )

    # Requirements
    op.create_table(
        'requirements',
        sa.Column('id', UUID(as_uuid=True), primary_key=True),
        sa.Column('tender_id', UUID(as_uuid=True), sa.ForeignKey('tenders.id'), nullable=False),
        sa.Column('version', sa.Integer(), nullable=False),
        sa.Column('type', sa.String(), nullable=False),
        sa.Column('value', JSONB(), nullable=False),
        sa.Column('mandatory', sa.Boolean(), nullable=False, server_default='true'),
        sa.Column('source_file', UUID(as_uuid=True), nullable=True),
        sa.Column('page', sa.Integer(), nullable=True),
        sa.Column('clause', sa.String(), nullable=True),
        sa.Column('confidence', sa.Float(), nullable=True),
    )

    # Matches
    op.create_table(
        'matches',
        sa.Column('id', UUID(as_uuid=True), primary_key=True),
        sa.Column('tenant_id', UUID(as_uuid=True), sa.ForeignKey('tenants.id'), nullable=False),
        sa.Column('tender_id', UUID(as_uuid=True), sa.ForeignKey('tenders.id'), nullable=False),
        sa.Column('score', sa.Integer(), nullable=True),
        sa.Column('decision', sa.String(), nullable=True),
        sa.Column('reasons', JSONB(), nullable=True),
    )

    # Bids
    op.create_table(
        'bids',
        sa.Column('id', UUID(as_uuid=True), primary_key=True),
        sa.Column('tenant_id', UUID(as_uuid=True), sa.ForeignKey('tenants.id'), nullable=False),
        sa.Column('tender_id', UUID(as_uuid=True), sa.ForeignKey('tenders.id'), nullable=False),
        sa.Column('status', sa.String(), nullable=False),
        sa.Column('approved_by', sa.String(), nullable=True),
    )
    
    # Audit Log
    op.create_table(
        'audit_log',
        sa.Column('id', sa.BigInteger(), primary_key=True, autoincrement=True),
        sa.Column('tenant_id', UUID(as_uuid=True), sa.ForeignKey('tenants.id'), nullable=False),
        sa.Column('actor', sa.String(), nullable=False),
        sa.Column('action', sa.String(), nullable=False),
        sa.Column('entity', sa.String(), nullable=False),
        sa.Column('detail', JSONB(), nullable=True),
        sa.Column('prev_hash', sa.String(), nullable=True),
        sa.Column('hash', sa.String(), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
    )
    # Revoke update/delete on audit_log for the app role (done in DB level or using triggers depending on pg setup)
    
    # Indexes
    op.create_index('ix_tenders_closes_at', 'tenders', ['closes_at'])
    op.create_index('ix_matches_tenant_score', 'matches', ['tenant_id', 'score'])
    op.create_index('ix_documents_tenant_expires', 'documents', ['tenant_id', 'expires_on'])


def downgrade() -> None:
    op.drop_table('audit_log')
    op.drop_table('bids')
    op.drop_table('matches')
    op.drop_table('requirements')
    op.drop_table('tender_files')
    op.drop_table('tender_versions')
    op.drop_table('tenders')
    op.drop_table('documents')
    op.drop_table('company_profile')
    op.drop_table('users')
    op.drop_table('tenants')
    op.execute("DROP EXTENSION IF EXISTS vector")
