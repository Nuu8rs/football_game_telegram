"""add_new_column_character_in_duel_from_reminder_character

Revision ID: 5706316bd271
Revises: b6d1da527139
Create Date: 2024-10-12 22:28:09.736124

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '5706316bd271'
down_revision: Union[str, None] = 'b6d1da527139'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('reminder_characters', sa.Column('character_in_duel', sa.Boolean(), server_default='0', nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('reminder_characters', 'character_in_duel')
    # ### end Alembic commands ###