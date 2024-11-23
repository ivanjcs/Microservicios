"""Pago

Revision ID: 7288f5a06ec9
Revises: e637cccf2c79
Create Date: 2024-10-22 22:29:36.751445

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '7288f5a06ec9'
down_revision = 'e637cccf2c79'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('pagos',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('producto_id', sa.Integer(), nullable=False),
    sa.Column('precio', sa.Float(), nullable=False),
    sa.Column('medio_pago', sa.String(length=120), nullable=False),
    sa.Column('deleted_at', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('pagos')
    # ### end Alembic commands ###
