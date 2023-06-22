"""Added cart

Revision ID: 0cbe8ef96e5e
Revises: 8b0ba1c4e6b7
Create Date: 2023-06-22 17:14:20.979265

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "0cbe8ef96e5e"
down_revision = "8b0ba1c4e6b7"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "cart",
        sa.Column("user_id", sa.UUID(), nullable=False),
        sa.Column("good_id", sa.UUID(), nullable=False),
        sa.Column("size_id", sa.UUID(), nullable=True),
        sa.Column("count", sa.Integer(), nullable=False),
        sa.Column("id", sa.UUID(), nullable=False),
        sa.ForeignKeyConstraint(
            ["good_id"],
            ["good.id"],
        ),
        sa.ForeignKeyConstraint(
            ["size_id"],
            ["size.id"],
        ),
        sa.ForeignKeyConstraint(
            ["user_id"],
            ["user.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("cart")
    # ### end Alembic commands ###
