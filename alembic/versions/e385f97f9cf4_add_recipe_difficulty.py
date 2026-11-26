
"""Add recipe difficulty

Revision ID: e385f97f9cf4
Revises: e8775be32dd2
Create Date: 2026-11-26 14:47:50.509070
"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = "e385f97f9cf4"
down_revision: Union[str, Sequence[str], None] = "e8775be32dd2"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    with op.batch_alter_table("recipe") as batch_op:
        batch_op.add_column(
            sa.Column("difficulty", sa.String(length=10), nullable=False)
        )

        batch_op.create_check_constraint(
            "ck_recipe_difficulty",
            "difficulty IN ('easy', 'medium', 'hard')"
        )


def downgrade() -> None:
    with op.batch_alter_table("recipe") as batch_op:
        batch_op.drop_constraint(
            "ck_recipe_difficulty",
            type_="check"
        )
        batch_op.drop_column("difficulty")
