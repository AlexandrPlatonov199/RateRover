"""empty message

Revision ID: 0986806bf325
Revises: 
Create Date: 2024-01-31 15:47:42.329329

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '0986806bf325'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('currency_courses',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('exchanger', sa.String(), nullable=False),
    sa.Column('direction', sa.String(), nullable=False),
    sa.Column('value', sa.Float(), nullable=False),
    sa.Column('updated_at', sa.DateTime(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('currency_courses')
    # ### end Alembic commands ###