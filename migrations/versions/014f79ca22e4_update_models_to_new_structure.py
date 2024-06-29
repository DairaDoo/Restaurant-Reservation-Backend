"""Update models to new structure

Revision ID: 014f79ca22e4
Revises: 479c47a56852
Create Date: 2024-06-27 15:38:41.686458

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '014f79ca22e4'
down_revision = '479c47a56852'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.add_column(sa.Column('first_name', sa.String(length=50), nullable=False, server_default='default_first_name'))
        batch_op.add_column(sa.Column('last_name', sa.String(length=50), nullable=False, server_default='default_last_name'))
        batch_op.add_column(sa.Column('phone_number', sa.String(length=20), nullable=False, server_default='0000000000'))
    # ### end Alembic commands ###




def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('users', schema=None) as batch_op:
        batch_op.add_column(sa.Column('username', sa.VARCHAR(length=80), nullable=False))
        batch_op.add_column(sa.Column('password', sa.VARCHAR(length=200), nullable=False))
        batch_op.drop_column('phone_number')
        batch_op.drop_column('last_name')
        batch_op.drop_column('first_name')

    # ### end Alembic commands ###
