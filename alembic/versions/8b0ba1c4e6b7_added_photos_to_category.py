"""Added photos to category

Revision ID: 8b0ba1c4e6b7
Revises: 26332a29bc04
Create Date: 2023-06-22 13:25:29.017494

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "8b0ba1c4e6b7"
down_revision = "26332a29bc04"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "categoryphoto",
        sa.Column("category_id", sa.UUID(), nullable=False),
        sa.Column("bucket_name", sa.String(), nullable=False),
        sa.Column("image_name", sa.String(), nullable=False),
        sa.Column("id", sa.UUID(), nullable=False),
        sa.ForeignKeyConstraint(
            ["category_id"],
            ["category.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("category_id"),
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("categoryphoto")
    # ### end Alembic commands ###
