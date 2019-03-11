"""create_likes

Revision ID: 5df2bf21d97a
Revises: de86b1026686
Create Date: 2019-03-07 17:05:11.931193

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '5df2bf21d97a'
down_revision = 'de86b1026686'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('likes',
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('likeimg_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['likeimg_id'], ['imgs.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('user_id', 'likeimg_id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('likes')
    # ### end Alembic commands ###