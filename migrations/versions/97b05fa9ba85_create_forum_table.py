"""create forum table

Revision ID: 97b05fa9ba85
Revises: 
Create Date: 2025-01-23 18:47:15.204058

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '97b05fa9ba85'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('role',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=50), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name')
    )
    op.create_table('user_role',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.String(length=255), nullable=False),
    sa.Column('role_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['role_id'], ['role.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('forum',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=100), nullable=False),
    sa.Column('description', sa.String(length=255), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.Column('author_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['author_id'], ['user_role.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('thread',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(length=255), nullable=False),
    sa.Column('post_count', sa.Integer(), nullable=True),
    sa.Column('last_post_at', sa.DateTime(), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.Column('updated_at', sa.DateTime(), nullable=True),
    sa.Column('forum_id', sa.Integer(), nullable=False),
    sa.Column('author_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['author_id'], ['user_role.id'], ),
    sa.ForeignKeyConstraint(['forum_id'], ['forum.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('thread')
    op.drop_table('forum')
    op.drop_table('user_role')
    op.drop_table('role')
    # ### end Alembic commands ###
