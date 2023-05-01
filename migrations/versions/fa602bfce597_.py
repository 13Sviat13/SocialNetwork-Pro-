"""empty message

Revision ID: fa602bfce597
Revises: 40fc148b4164
Create Date: 2023-05-01 16:40:17.073228

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'fa602bfce597'
down_revision = '40fc148b4164'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('profiles', schema=None) as batch_op:
        batch_op.add_column(sa.Column('Linkedln_URL', sa.String(), nullable=True))
        batch_op.add_column(sa.Column('Facebook_URL', sa.String(), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('profiles', schema=None) as batch_op:
        batch_op.drop_column('Facebook_URL')
        batch_op.drop_column('Linkedln_URL')

    # ### end Alembic commands ###