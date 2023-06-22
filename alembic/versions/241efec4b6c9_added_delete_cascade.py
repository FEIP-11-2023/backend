"""Added delete cascade

Revision ID: 241efec4b6c9
Revises: 73764176e1f0
Create Date: 2023-06-22 21:26:54.137025

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "241efec4b6c9"
down_revision = "73764176e1f0"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint("sale_good_id_fkey", "sale", type_="foreignkey")
    op.create_foreign_key(None, "sale", "good", ["good_id"], ["id"], ondelete="CASCADE")
    op.create_unique_constraint(None, "size", ["good_id", "size"])
    op.drop_constraint("size_good_id_fkey", "size", type_="foreignkey")
    op.create_foreign_key(None, "size", "good", ["good_id"], ["id"], ondelete="CASCADE")
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, "size", type_="foreignkey")
    op.create_foreign_key("size_good_id_fkey", "size", "good", ["good_id"], ["id"])
    op.drop_constraint(None, "size", type_="unique")
    op.drop_constraint(None, "sale", type_="foreignkey")
    op.create_foreign_key("sale_good_id_fkey", "sale", "good", ["good_id"], ["id"])
    # ### end Alembic commands ###
