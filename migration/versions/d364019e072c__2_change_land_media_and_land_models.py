"""_2_change land media and land models

Revision ID: d364019e072c
Revises: f7d71d0d8cc3
Create Date: 2024-12-02 11:50:42.284886

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = 'd364019e072c'
down_revision: Union[str, None] = 'f7d71d0d8cc3'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('land_media',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('url', sa.String(), nullable=False),
    sa.Column('land_id', sa.Integer(), nullable=False),
    sa.Column('created_at', sa.TIMESTAMP(timezone=True), nullable=False),
    sa.Column('updated_at', sa.TIMESTAMP(timezone=True), nullable=False),
    sa.ForeignKeyConstraint(['land_id'], ['land.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_land_media_id'), 'land_media', ['id'], unique=False)
    op.drop_index('ix_land_image_id', table_name='land_image')
    op.drop_table('land_image')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('land_image',
    sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False),
    sa.Column('url', sa.VARCHAR(), autoincrement=False, nullable=False),
    sa.Column('land_id', sa.INTEGER(), autoincrement=False, nullable=False),
    sa.Column('created_at', postgresql.TIMESTAMP(timezone=True), autoincrement=False, nullable=False),
    sa.Column('updated_at', postgresql.TIMESTAMP(timezone=True), autoincrement=False, nullable=False),
    sa.ForeignKeyConstraint(['land_id'], ['land.id'], name='land_image_land_id_fkey'),
    sa.PrimaryKeyConstraint('id', name='land_image_pkey')
    )
    op.create_index('ix_land_image_id', 'land_image', ['id'], unique=False)
    op.drop_index(op.f('ix_land_media_id'), table_name='land_media')
    op.drop_table('land_media')
    # ### end Alembic commands ###