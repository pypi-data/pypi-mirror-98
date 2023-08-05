"""Added column aggregated_at to CVE

Revision ID: 9b210f8d5c24
Revises: 79e1d320db3d
Create Date: 2019-12-06 19:08:16.125613+00:00

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '9b210f8d5c24'
down_revision = '79e1d320db3d'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('cve', sa.Column('aggregated_at', sa.DateTime(), nullable=True))
    op.alter_column('cve', 'cve_id',
               existing_type=sa.VARCHAR(length=256),
               nullable=False)
    op.create_unique_constraint(None, 'cve', ['cve_id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'cve', type_='unique')
    op.alter_column('cve', 'cve_id',
               existing_type=sa.VARCHAR(length=256),
               nullable=True)
    op.drop_column('cve', 'aggregated_at')
    # ### end Alembic commands ###
