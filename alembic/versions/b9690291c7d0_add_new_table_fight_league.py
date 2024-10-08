"""add_new_table_fight_league

Revision ID: b9690291c7d0
Revises: 812064143a86
Create Date: 2024-08-22 02:16:08.907437

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'b9690291c7d0'
down_revision: Union[str, None] = '812064143a86'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('league_fight',
    sa.Column('id', sa.BigInteger(), nullable=False),
    sa.Column('match_id', sa.String(length=255), nullable=False),
    sa.Column('time_to_start', sa.DateTime(), nullable=True),
    sa.Column('first_club_id', sa.BigInteger(), nullable=False),
    sa.Column('second_club_id', sa.BigInteger(), nullable=False),
    sa.Column('goal_first_club', sa.Integer(), nullable=True),
    sa.Column('goal_second_club', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['first_club_id'], ['clubs.id'], ),
    sa.ForeignKeyConstraint(['second_club_id'], ['clubs.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('match_id') 
    )
    op.create_index(op.f('ix_league_fight_id'), 'league_fight', ['id'], unique=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_league_fight_id'), table_name='league_fight')
    op.drop_table('league_fight')
    # ### end Alembic commands ###
