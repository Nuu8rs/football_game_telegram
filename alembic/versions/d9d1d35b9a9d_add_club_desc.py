"""add club desc

Revision ID: d9d1d35b9a9d
Revises: 7f6c84aad7d0
Create Date: 2025-05-02 18:11:26.420633

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision: str = 'd9d1d35b9a9d'
down_revision: Union[str, None] = '7f6c84aad7d0'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('clubs', sa.Column('description', sa.String(length=255), server_default='Не вказано', nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('clubs', 'description')
    # ### end Alembic commands ###
