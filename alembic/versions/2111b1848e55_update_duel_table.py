"""update_duel_table

Revision ID: 2111b1848e55
Revises: 55885cd118a2
Create Date: 2024-10-20 02:15:14.115974

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '2111b1848e55'
down_revision: Union[str, None] = '55885cd118a2'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('duels', sa.Column('duel_id', sa.String(length=255), nullable=False))
    op.add_column('duels', sa.Column('created_time', sa.DateTime(), nullable=False))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('duels', 'created_time')
    op.drop_column('duels', 'duel_id')
    # ### end Alembic commands ###