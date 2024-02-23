"""update pet table

Revision ID: aa1135c74727
Revises: 33a1e6eb4dda
Create Date: 2024-02-24 01:19:12.050028

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'aa1135c74727'
down_revision: Union[str, None] = '33a1e6eb4dda'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('pet', sa.Column('birthday', sa.Date(), nullable=True))
    op.add_column('pet', sa.Column('role', sa.String(), nullable=False))
    op.drop_column('pet', 'age')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('pet', sa.Column('age', sa.INTEGER(), autoincrement=False, nullable=True))
    op.drop_column('pet', 'role')
    op.drop_column('pet', 'birthday')
    # ### end Alembic commands ###
