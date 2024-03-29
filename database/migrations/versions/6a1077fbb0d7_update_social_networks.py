"""Update social networks

Revision ID: 6a1077fbb0d7
Revises: 782997ad2bce
Create Date: 2024-02-25 04:20:48.743918

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '6a1077fbb0d7'
down_revision: Union[str, None] = '782997ad2bce'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('social_network', 'link',
               existing_type=sa.VARCHAR(),
               nullable=False)
    op.alter_column('social_network', 'is_public',
               existing_type=sa.BOOLEAN(),
               nullable=False)
    op.alter_column('social_network', 'created_at',
               existing_type=postgresql.TIMESTAMP(),
               nullable=False)
    op.alter_column('social_network', 'user_id',
               existing_type=sa.BIGINT(),
               nullable=False)
    op.alter_column('social_network', 'social_network_type_id',
               existing_type=sa.BIGINT(),
               nullable=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('social_network', 'social_network_type_id',
               existing_type=sa.BIGINT(),
               nullable=True)
    op.alter_column('social_network', 'user_id',
               existing_type=sa.BIGINT(),
               nullable=True)
    op.alter_column('social_network', 'created_at',
               existing_type=postgresql.TIMESTAMP(),
               nullable=True)
    op.alter_column('social_network', 'is_public',
               existing_type=sa.BOOLEAN(),
               nullable=True)
    op.alter_column('social_network', 'link',
               existing_type=sa.VARCHAR(),
               nullable=True)
    # ### end Alembic commands ###
