"""add email to user table

Revision ID: 8ce03d5c5cb9
Revises: 0fe1e1bafcf0
Create Date: 2023-04-09 22:54:28.019617

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '8ce03d5c5cb9'
down_revision = '0fe1e1bafcf0'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.add_column(sa.Column('email', sa.String(), nullable=True))
        batch_op.create_index(batch_op.f('ix_user_email'), ['email'], unique=True)


    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_user_email'))
        batch_op.drop_column('email')

    # ### end Alembic commands ###