"""add new column to club

Revision ID: a34028cb8757
Revises: 379813cf6a10
Create Date: 2024-11-14 14:12:56.906797

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'a34028cb8757'
down_revision: Union[str, None] = '379813cf6a10'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('clubs', sa.Column('custom_url_photo_stadion', sa.String(length=255), server_default='src\\fight_club_menu.jpg', nullable=False))
    op.add_column('clubs', sa.Column('custom_name_stadion', sa.String(length=255), server_default='Стадіон', nullable=False))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('clubs', 'custom_name_stadion')
    op.drop_column('clubs', 'custom_url_photo_stadion')
    # ### end Alembic commands ###
