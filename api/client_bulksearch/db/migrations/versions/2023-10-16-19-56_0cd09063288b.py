"""empty message

Revision ID: 0cd09063288b
Revises: 2b7380507a71
Create Date: 2023-10-16 19:56:55.037642

"""
import fastapi_users_db_sqlalchemy
import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "0cd09063288b"
down_revision = "2b7380507a71"
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "appuser",
        sa.Column("id", fastapi_users_db_sqlalchemy.generics.GUID(), nullable=False),
        sa.Column("email", sa.String(length=320), nullable=False),
        sa.Column("hashed_password", sa.String(length=1024), nullable=False),
        sa.Column("is_active", sa.Boolean(), nullable=False),
        sa.Column("is_superuser", sa.Boolean(), nullable=False),
        sa.Column("is_verified", sa.Boolean(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(op.f("ix_appuser_email"), "appuser", ["email"], unique=True)
    op.alter_column(
        "dummy_model", "name", existing_type=sa.VARCHAR(length=200), nullable=False
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column(
        "dummy_model", "name", existing_type=sa.VARCHAR(length=200), nullable=True
    )
    op.drop_index(op.f("ix_appuser_email"), table_name="appuser")
    op.drop_table("appuser")
    # ### end Alembic commands ###
