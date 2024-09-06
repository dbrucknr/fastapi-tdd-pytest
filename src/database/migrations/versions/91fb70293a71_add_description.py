"""add description

Revision ID: 91fb70293a71
Revises: b03bce6c19b5
Create Date: 2024-09-06 16:21:49.505688

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import sqlmodel    


# revision identifiers, used by Alembic.
revision: str = '91fb70293a71'
down_revision: Union[str, None] = 'b03bce6c19b5'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('category', sa.Column('description', sqlmodel.sql.sqltypes.AutoString(), nullable=False))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('category', 'description')
    # ### end Alembic commands ###
