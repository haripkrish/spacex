"""spacex init

Revision ID: 677fc09721a2
Revises: 
Create Date: 2023-08-31 23:21:40.314688

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '677fc09721a2'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table('launches',
                    sa.Column('id', sa.String(), nullable=False, primary_key=True),
                    sa.Column('name', sa.String(), nullable=True),
                    sa.Column('details', sa.String(), nullable=True),
                    sa.Column('rocket_id', sa.String(), nullable=True),
                    sa.Column('rocket_name', sa.String(), nullable=True),
                    sa.Column('flight_number', sa.Integer(), nullable=True),
                    sa.Column('success', sa.Boolean(), nullable=True),

                    sa.Column('launch_date_utc', sa.DateTime(timezone=True), nullable=True),
                    sa.Column('launch_date_local', sa.DateTime(timezone=True), nullable=True),
                    sa.Column('launch_date_precision', sa.String(), nullable=True),
                    sa.Column('launch_date_unix', sa.Integer(), nullable=True),

                    sa.Column('transformed_at_utc', sa.DateTime(timezone=True), nullable=False),
                    sa.Column('transformed_at_date', sa.Date(), nullable=False),
                    )


def downgrade() -> None:
    op.drop_table('launches')
