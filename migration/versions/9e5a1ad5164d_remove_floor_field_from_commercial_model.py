"""remove floor field from commercial model

Revision ID: 9e5a1ad5164d
Revises: 32072da668f4
Create Date: 2024-12-07 00:00:50.330822

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '9e5a1ad5164d'
down_revision: Union[str, None] = '32072da668f4'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('commercial', 'floor')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('commercial', sa.Column('floor', sa.INTEGER(), autoincrement=False, nullable=False))
    # ### end Alembic commands ###
