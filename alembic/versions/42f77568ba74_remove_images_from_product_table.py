"""remove images from product table

Revision ID: 42f77568ba74
Revises: 622268d009e1
Create Date: 2025-05-18 18:23:34.788894

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '42f77568ba74'
down_revision: Union[str, None] = '622268d009e1'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.drop_column('product', 'images')


def downgrade():
    op.add_column('product', sa.Column('images', sa.String))
