"""Books model changed

Revision ID: db4eb846e9c7
Revises: 9feaf19d31ad
Create Date: 2024-03-12 20:33:37.676462

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'db4eb846e9c7'
down_revision = '9feaf19d31ad'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('books', schema=None) as batch_op:
        batch_op.alter_column('title',
               existing_type=sa.VARCHAR(length=50),
               type_=sa.String(length=200),
               existing_nullable=True)
        batch_op.alter_column('authors',
               existing_type=sa.VARCHAR(length=50),
               type_=sa.String(length=200),
               existing_nullable=True)
        batch_op.alter_column('publisher',
               existing_type=sa.VARCHAR(length=50),
               type_=sa.String(length=200),
               existing_nullable=True)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('books', schema=None) as batch_op:
        batch_op.alter_column('publisher',
               existing_type=sa.String(length=200),
               type_=sa.VARCHAR(length=50),
               existing_nullable=True)
        batch_op.alter_column('authors',
               existing_type=sa.String(length=200),
               type_=sa.VARCHAR(length=50),
               existing_nullable=True)
        batch_op.alter_column('title',
               existing_type=sa.String(length=200),
               type_=sa.VARCHAR(length=50),
               existing_nullable=True)

    # ### end Alembic commands ###
