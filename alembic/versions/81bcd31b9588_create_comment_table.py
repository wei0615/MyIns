"""create comment table

Revision ID: 81bcd31b9588
Revises: 7d48516944e3
Create Date: 2019-01-11 16:50:00.327955

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '81bcd31b9588'
down_revision = '7d48516944e3'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('comments',
    sa.Column('img_id', sa.Integer(), nullable=False),
    sa.Column('comments', sa.String(length=200), nullable=True),
    sa.ForeignKeyConstraint(['img_id'], ['imgs.id'], ),
    sa.PrimaryKeyConstraint('img_id')
    )
    op.drop_column('imgs', 'comment')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('imgs', sa.Column('comment', mysql.VARCHAR(length=100), nullable=True))
    op.drop_table('comments')
    # ### end Alembic commands ###
