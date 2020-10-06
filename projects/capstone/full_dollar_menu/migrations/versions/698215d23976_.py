"""empty message

Revision ID: 698215d23976
Revises: 
Create Date: 2020-10-06 15:57:17.361838

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '698215d23976'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('catagories')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('catagories',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('type', sa.VARCHAR(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###
