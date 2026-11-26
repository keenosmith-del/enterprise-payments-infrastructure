"""Add synthetic identity references and technical application configuration."""
from alembic import op
import sqlalchemy as sa

revision = "m01_principals"
down_revision = "m01_initial"
branch_labels = None
depends_on = None


def upgrade():
    op.create_table("foundation_principal", sa.Column("id", sa.Uuid(), primary_key=True),
                    sa.Column("tenant_id", sa.Uuid(), sa.ForeignKey("tenant.id"), nullable=False),
                    sa.Column("identity_reference", sa.String(120), nullable=False),
                    sa.Column("kind", sa.String(16), nullable=False),
                    sa.CheckConstraint("kind IN ('human', 'service')", name="principal_kind_check"),
                    sa.UniqueConstraint("tenant_id", "identity_reference"))
    op.create_table("application_config", sa.Column("tenant_id", sa.Uuid(), sa.ForeignKey("tenant.id"), primary_key=True),
                    sa.Column("key", sa.String(120), primary_key=True),
                    sa.Column("value", sa.String(240), nullable=False))


def downgrade():
    op.drop_table("application_config")
    op.drop_table("foundation_principal")
