from alembic import op
import sqlalchemy as sa

"""ajouter alembic"""


def upgrade():
    op.create_table(
        "donnees",
        sa.Column("id", sa.Integer, primary_key=True, autoincrement=True),
        sa.Column("donnee", sa.Text(), nullable=False),
    )


def downgrade():
    op.drop_table("donnees")
