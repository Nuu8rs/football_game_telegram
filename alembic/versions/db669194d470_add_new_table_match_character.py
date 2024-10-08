"""add_new_table_match_character

Revision ID: db669194d470
Revises: b315aefd092f
Create Date: 2024-09-18 17:43:00.373918

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision: str = 'db669194d470'
down_revision: Union[str, None] = 'b315aefd092f'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('match_character',
        sa.Column('id', sa.BigInteger(), nullable=False),
        sa.Column('character_id', sa.BigInteger(), nullable=True),
        sa.Column('match_id', sa.String(length=255), nullable=False),
        sa.Column('group_id', sa.String(length=255), nullable=False),
        sa.Column('club_id', sa.Integer(), nullable=False),
        sa.Column('goals_count', sa.Integer(), server_default='0', nullable=False),
        sa.ForeignKeyConstraint(['character_id'], ['characters.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['match_id'], ['league_fight.match_id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id'),
    )
    op.create_index(op.f('ix_match_character_id'), 'match_character', ['id'], unique=False)

    op.create_table('reminder_characters',
        sa.Column('id', sa.BigInteger(), nullable=False),
        sa.Column('character_id', sa.BigInteger(), nullable=True),
        sa.Column('character_in_training', sa.Boolean(), nullable=True),
        sa.Column('training_stats', sa.String(length=255), nullable=True),
        sa.Column('time_start_training', sa.DateTime(), nullable=True),
        sa.Column('time_training_seconds', sa.BigInteger(), nullable=True),
        sa.Column('education_reward_date', sa.DateTime(), server_default=sa.text("'1970-01-01 00:00:00'"), nullable=False),
        sa.Column('time_to_join_club', sa.DateTime(), server_default=sa.text("'1970-01-01 00:00:00'"), nullable=False),
        sa.ForeignKeyConstraint(['character_id'], ['characters.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id'),
    )
    op.create_index(op.f('ix_reminder_characters_id'), 'reminder_characters', ['id'], unique=False)

    op.drop_column('characters', 'education_reward_date')
    op.drop_column('characters', 'time_to_join_club')
    op.drop_column('characters', 'character_in_training')
    # ### end Alembic commands ###

def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('characters', sa.Column('character_in_training', mysql.TINYINT(display_width=1), autoincrement=False, nullable=True))
    op.add_column('characters', sa.Column('time_to_join_club', mysql.DATETIME(), server_default=sa.text("'1970-01-01 00:00:00'"), nullable=True))
    op.add_column('characters', sa.Column('education_reward_date', mysql.DATETIME(), server_default=sa.text("'1970-01-01 00:00:00'"), nullable=True))
    op.drop_index(op.f('ix_reminder_characters_id'), table_name='reminder_characters')
    op.drop_table('reminder_characters')
    op.drop_index(op.f('ix_match_character_id'), table_name='match_character')
    op.drop_table('match_character')
    # ### end Alembic commands ###
