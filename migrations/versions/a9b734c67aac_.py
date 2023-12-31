"""empty message

Revision ID: a9b734c67aac
Revises: 24fec12ae850
Create Date: 2023-12-10 18:39:00.439441

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a9b734c67aac'
down_revision = '24fec12ae850'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('metric',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('metric', sa.String(length=140), nullable=False),
    sa.Column('value', sa.Float(), nullable=False),
    sa.Column('experiment_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['experiment_id'], ['experiment.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    with op.batch_alter_table('metric', schema=None) as batch_op:
        batch_op.create_index(batch_op.f('ix_metric_experiment_id'), ['experiment_id'], unique=False)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('metric', schema=None) as batch_op:
        batch_op.drop_index(batch_op.f('ix_metric_experiment_id'))

    op.drop_table('metric')
    # ### end Alembic commands ###
