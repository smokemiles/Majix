"""note_pic updte

Revision ID: 670b75f90255
Revises: 5537683485e8
Create Date: 2025-06-04 14:47:26.651495

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '670b75f90255'
down_revision = '5537683485e8'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('notes', schema=None) as batch_op:
        batch_op.add_column(sa.Column('notepic', sa.String(length=255), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('notes', schema=None) as batch_op:
        batch_op.drop_column('notepic')

    # ### end Alembic commands ###
