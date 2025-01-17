"""change user model

Revision ID: a8eba366373e
Revises: c0c6c590b223
Create Date: 2025-01-17 17:36:07.998024

"""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision: str = "a8eba366373e"
down_revision: Union[str, None] = "c0c6c590b223"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table("users", schema=None) as batch_op:
        batch_op.drop_constraint("users_email_key", type_="unique")
        batch_op.drop_constraint("users_username_key", type_="unique")

    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table("users", schema=None) as batch_op:
        batch_op.create_unique_constraint("users_username_key", ["username"])
        batch_op.create_unique_constraint("users_email_key", ["email"])

    # ### end Alembic commands ###
