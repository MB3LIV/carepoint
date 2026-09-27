"""add consultation fee to doctor

Revision ID: ba2f3912f478
Revises: ff288a5c7c60
Create Date: 2026-09-27 11:21:56.479150

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = 'ba2f3912f478'
down_revision = 'ff288a5c7c60'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('Doctors', sa.Column('consultation_fee', sa.Numeric(precision=10, scale=2), nullable=False, server_default='0.00'))


def downgrade():
    op.drop_column('Doctors', 'consultation_fee')