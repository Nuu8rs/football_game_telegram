"""add_new_column_time_edit_schema_in_table_clubs

Revision ID: bf4444fb896d
Revises: ab7f83f56211
Create Date: 2024-10-01 15:56:06.449707

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'bf4444fb896d'
down_revision: Union[str, None] = 'ab7f83f56211'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('clubs', sa.Column('time_edit_schema', sa.DateTime(), server_default=sa.text("'1970-01-01 00:00:00'"), nullable=False))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('clubs', 'time_edit_schema')
    # ### end Alembic commands ###