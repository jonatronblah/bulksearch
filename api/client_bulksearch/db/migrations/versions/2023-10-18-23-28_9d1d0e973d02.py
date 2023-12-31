"""empty message

Revision ID: 9d1d0e973d02
Revises: 0cd09063288b
Create Date: 2023-10-18 23:28:31.027186

"""
import fastapi_users_db_sqlalchemy
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "9d1d0e973d02"
down_revision = "0cd09063288b"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column(
        "appuser", sa.Column("username", sa.String(length=200), nullable=False)
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column("appuser", "username")
    # ### end Alembic commands ###
