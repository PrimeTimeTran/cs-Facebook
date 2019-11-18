"""empty message

Revision ID: 6f30bf1d3918
Revises: 
Create Date: 2019-11-18 10:50:05.005633

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '6f30bf1d3918'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('users')
    op.drop_table('reaction')
    op.add_column('post', sa.Column('view_count', sa.Integer(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('post', 'view_count')
    op.create_table('reaction',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('user_id', sa.INTEGER(), nullable=True),
    sa.Column('post_id', sa.INTEGER(), nullable=True),
    sa.Column('reaction_type', sa.VARCHAR(length=7), nullable=False),
    sa.CheckConstraint("reaction_type IN ('liked', 'laughed', 'wowed', 'frowned', 'loved')", name='reactionenum'),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('users',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('email', sa.VARCHAR(length=100), nullable=True),
    sa.Column('password', sa.VARCHAR(length=255), nullable=True),
    sa.Column('avatar_url', sa.TEXT(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email')
    )
    # ### end Alembic commands ###
