"""empty message

Revision ID: 7663caab3cd8
Revises: 9a6f11b5dc89
Create Date: 2024-05-21 21:23:43.142540

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '7663caab3cd8'
down_revision = '9a6f11b5dc89'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('board',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('name', sa.String(length=20), nullable=False),
    sa.Column('priority', sa.Integer(), nullable=True),
    sa.Column('create_time', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('board')
    # ### end Alembic commands ###