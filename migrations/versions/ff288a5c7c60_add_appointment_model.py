"""add appointment model

Revision ID: ff288a5c7c60
Revises: 0e1d61d09dcf
Create Date: 2026-09-27 11:05:23.880299

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = 'ff288a5c7c60'
down_revision = '0e1d61d09dcf'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('Appointments',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('doctor_id', sa.Integer(), nullable=False),
    sa.Column('appointment_date', sa.Date(), nullable=False),
    sa.Column('appointment_time', sa.Time(), nullable=False),
    sa.Column('reason', sa.String(length=255), nullable=True),
    sa.Column('status', sa.Enum('Pending', 'Accepted', 'Rejected', 'Cancelled', 'Completed', name='appointment_status'), nullable=False),
    sa.ForeignKeyConstraint(['doctor_id'], ['Doctors.id'], ),
    sa.PrimaryKeyConstraint('id')
    )


def downgrade():
    op.drop_table('Appointments')