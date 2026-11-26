"""Initial non-financial foundation records."""
from alembic import op
import sqlalchemy as sa

revision = "m01_initial"
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table("tenant", sa.Column("id", sa.Uuid(), primary_key=True),
                    sa.Column("name", sa.String(120), nullable=False, unique=True))
    op.create_table("legal_entity", sa.Column("id", sa.Uuid(), primary_key=True),
                    sa.Column("tenant_id", sa.Uuid(), sa.ForeignKey("tenant.id"), nullable=False),
                    sa.Column("name", sa.String(120), nullable=False),
                    sa.UniqueConstraint("tenant_id", "name"))


def downgrade():
    op.drop_table("legal_entity")
    op.drop_table("tenant")
