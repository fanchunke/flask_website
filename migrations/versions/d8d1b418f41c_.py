"""empty message

Revision ID: d8d1b418f41c
Revises: 7f5c9e993be1
Create Date: 2017-02-15 21:03:05.958000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'd8d1b418f41c'
down_revision = '7f5c9e993be1'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('profiles',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('nickname', sa.String(length=10), nullable=False),
    sa.Column('gender', sa.String(length=4), nullable=False),
    sa.Column('address', sa.String(length=4), nullable=True),
    sa.Column('discription', sa.Text(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('profiles')
    # ### end Alembic commands ###