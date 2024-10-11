"""empty message

Revision ID: 8a47a67d5d6c
Revises: 805f4766855c
Create Date: 2024-10-11 03:18:26.413781

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '8a47a67d5d6c'
down_revision = '805f4766855c'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('members', schema=None) as batch_op:
        batch_op.alter_column('role_id',
               existing_type=sa.INTEGER(),
               nullable=True)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('members', schema=None) as batch_op:
        batch_op.alter_column('role_id',
               existing_type=sa.INTEGER(),
               nullable=False)

    # ### end Alembic commands ###
