"""empty message

Revision ID: b1950e867333
Revises: 
Create Date: 2018-04-22 14:17:17.461295

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b1950e867333'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('rsvp', sa.Column('attendance', sa.Boolean(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('rsvp', 'attendance')
    # ### end Alembic commands ###