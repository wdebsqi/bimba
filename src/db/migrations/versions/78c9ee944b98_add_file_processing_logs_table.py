"""add file_processing_logs_table

Revision ID: 78c9ee944b98
Revises: 702d5deb5180
Create Date: 2023-06-17 19:21:41.983608

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '78c9ee944b98'
down_revision = '702d5deb5180'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('file_processing_logs',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('created_at', sa.DateTime(), nullable=False),
    sa.Column('file_name', sa.String(), nullable=False),
    sa.Column('file_contents_hash', sa.String(), nullable=False),
    sa.Column('processed_successfully', sa.Boolean(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('file_processing_logs')
    # ### end Alembic commands ###
