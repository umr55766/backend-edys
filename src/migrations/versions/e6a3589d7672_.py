"""empty message

Revision ID: e6a3589d7672
Revises: 
Create Date: 2018-11-30 17:44:07.787427

"""
from alembic import op
import sqlalchemy as sa
import sqlalchemy_utils


# revision identifiers, used by Alembic.
revision = 'e6a3589d7672'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('page_word_count',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('url', sqlalchemy_utils.types.url.URLType(), nullable=True),
    sa.Column('word_count', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('page_word_count')
    # ### end Alembic commands ###
