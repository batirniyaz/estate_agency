"""2_create current_status enum model

Revision ID: 4bf2135cc9b6
Revises: 289c2e196e30
Create Date: 2024-12-06 14:58:35.568999

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import ENUM


# revision identifiers, used by Alembic.
revision: str = '4bf2135cc9b6'
down_revision: Union[str, None] = '289c2e196e30'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

current_status_enum = ENUM('FREE', 'SOON', 'BUSY', name='currentstatus', create_type=False)


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###

    current_status_enum.create(op.get_bind(), checkfirst=True)

    op.add_column('apartment', sa.Column('current_status', sa.Enum('FREE', 'SOON', 'BUSY', name='currentstatus'), nullable=True))
    op.add_column('commercial', sa.Column('current_status', sa.Enum('FREE', 'SOON', 'BUSY', name='currentstatus'), nullable=True))
    op.add_column('land', sa.Column('current_status', sa.Enum('FREE', 'SOON', 'BUSY', name='currentstatus'), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('land', 'current_status')
    op.drop_column('commercial', 'current_status')
    op.drop_column('apartment', 'current_status')

    current_status_enum.drop(op.get_bind(), checkfirst=True)
    # ### end Alembic commands ###