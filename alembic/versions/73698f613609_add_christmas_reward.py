"""add christmas reward

Revision ID: 73698f613609
Revises: 7448fb71c996
Create Date: 2024-12-23 11:15:13.504618

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '73698f613609'
down_revision: Union[str, None] = '7448fb71c996'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('christmas_reward',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.BigInteger(), nullable=False),
    sa.Column('time_get', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['users.user_id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_christmas_reward_id'), 'christmas_reward', ['id'], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_christmas_reward_id'), table_name='christmas_reward')
    op.drop_table('christmas_reward')
    # ### end Alembic commands ###
