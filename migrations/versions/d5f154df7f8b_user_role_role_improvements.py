"""user role / role improvements

Revision ID: d5f154df7f8b
Revises: 967ecbc45d5f
Create Date: 2025-01-24 11:28:26.082964

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd5f154df7f8b'
down_revision = '967ecbc45d5f'
branch_labels = None
depends_on = None


def upgrade():
    # Step 1: Add the column with a default value (e.g., 1)
    op.add_column('role', sa.Column('role_id', sa.Integer(), nullable=True, server_default='1'))

    # Step 2: Set role_id for existing records if needed
    op.execute("UPDATE role SET role_id = 1 WHERE role_id IS NULL")

    # Step 3: Alter column to make it NOT NULL
    op.alter_column('role', 'role_id', nullable=False, server_default=None)

def downgrade():
    # Reverse the above steps
    op.alter_column('role', 'role_id', nullable=True)
    op.drop_column('role', 'role_id')
