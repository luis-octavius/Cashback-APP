"""create cashback_queries table

Revision ID: 20260415_01
Revises:
Create Date: 2026-04-15
"""

from alembic import op
import sqlalchemy as sa


revision = "20260415_01"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "cashback_queries",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("ip_address", sa.String(length=64), nullable=False),
        sa.Column("customer_type", sa.String(length=20), nullable=False),
        sa.Column("purchase_amount", sa.Numeric(10, 2), nullable=False),
        sa.Column("discount_percent", sa.Numeric(5, 2), nullable=False),
        sa.Column("final_amount", sa.Numeric(10, 2), nullable=False),
        sa.Column("cashback_amount", sa.Numeric(10, 2), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("now()"), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_cashback_queries_id", "cashback_queries", ["id"], unique=False)
    op.create_index("ix_cashback_queries_ip_address", "cashback_queries", ["ip_address"], unique=False)
    op.create_index("ix_cashback_queries_customer_type", "cashback_queries", ["customer_type"], unique=False)


def downgrade() -> None:
    op.drop_index("ix_cashback_queries_customer_type", table_name="cashback_queries")
    op.drop_index("ix_cashback_queries_ip_address", table_name="cashback_queries")
    op.drop_index("ix_cashback_queries_id", table_name="cashback_queries")
    op.drop_table("cashback_queries")
