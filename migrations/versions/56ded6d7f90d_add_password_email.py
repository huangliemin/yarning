"""add password email

Revision ID: 56ded6d7f90d
Revises: 1c5698276dbf
Create Date: 2015-03-12 15:41:26.406000

"""

# revision identifiers, used by Alembic.
revision = '56ded6d7f90d'
down_revision = '1c5698276dbf'

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.add_column('users', sa.Column('email', sa.String(length=64), nullable=True))
    op.add_column('users', sa.Column('password_hash', sa.String(length=128), nullable=True))
    op.create_index('ix_users_email', 'users', ['email'], unique=True)
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_index('ix_users_email', 'users')
    op.drop_column('users', 'password_hash')
    op.drop_column('users', 'email')
    ### end Alembic commands ###
