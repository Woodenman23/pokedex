"""pokedex table

Revision ID: 3a638c28a35c
Revises: bff34762998b
Create Date: 2024-12-10 14:55:05.929189

"""

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = "3a638c28a35c"
down_revision = "bff34762998b"
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "pokedex",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("name", sa.String(length=64), nullable=False),
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.Column("description", sa.String(length=512), nullable=False),
        sa.ForeignKeyConstraint(
            ["user_id"],
            ["user.id"],
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    with op.batch_alter_table("pokedex", schema=None) as batch_op:
        batch_op.create_index(
            batch_op.f("ix_pokedex_user_id"), ["user_id"], unique=False
        )

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table("pokedex", schema=None) as batch_op:
        batch_op.drop_index(batch_op.f("ix_pokedex_user_id"))

    op.drop_table("pokedex")
    # ### end Alembic commands ###