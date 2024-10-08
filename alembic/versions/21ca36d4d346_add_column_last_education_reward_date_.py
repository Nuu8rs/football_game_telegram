"""add_column_last_education_reward_date_in_character

Revision ID: 21ca36d4d346
Revises: 78c84de2aac3
Create Date: 2024-09-05 00:37:03.703332

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '21ca36d4d346'
down_revision: Union[str, None] = '78c84de2aac3'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('characters', sa.Column('last_reward_date', sa.DateTime(), server_default=sa.text("'1970-01-01 00:00:00'"), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('characters', 'last_reward_date')
    # ### end Alembic commands ###
