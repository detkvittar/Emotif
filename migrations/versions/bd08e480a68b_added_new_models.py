"""Added new models

Revision ID: bd08e480a68b
Revises: 
Create Date: 2024-02-09 02:31:42.400636

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'bd08e480a68b'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('post', schema=None) as batch_op:
        batch_op.add_column(sa.Column('hashtags', sa.String(length=255), nullable=True))
        batch_op.add_column(sa.Column('location', sa.String(length=255), nullable=True))

    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.add_column(sa.Column('profile_picture', sa.String(length=255), nullable=True))
        batch_op.add_column(sa.Column('bio', sa.Text(), nullable=True))
        batch_op.add_column(sa.Column('is_private', sa.Boolean(), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('user', schema=None) as batch_op:
        batch_op.drop_column('is_private')
        batch_op.drop_column('bio')
        batch_op.drop_column('profile_picture')

    with op.batch_alter_table('post', schema=None) as batch_op:
        batch_op.drop_column('location')
        batch_op.drop_column('hashtags')

    # ### end Alembic commands ###
