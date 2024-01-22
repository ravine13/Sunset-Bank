"""initial migration

Revision ID: 2ef8e61d6328
Revises: 
Create Date: 2024-01-21 19:12:32.282232

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2ef8e61d6328'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('client',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(length=50), nullable=False),
    sa.Column('password', sa.String(length=100), nullable=False),
    sa.Column('email', sa.String(length=100), nullable=False),
    sa.Column('phone_number', sa.String(length=15), nullable=True),
    sa.Column('date_joined', sa.DateTime(), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email'),
    sa.UniqueConstraint('phone_number'),
    sa.UniqueConstraint('username')
    )
    op.create_table('account',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('account_number', sa.String(length=20), nullable=False),
    sa.Column('balance', sa.Float(), nullable=True),
    sa.Column('account_type', sa.String(length=20), nullable=False),
    sa.Column('opened_at', sa.DateTime(), nullable=False),
    sa.Column('client_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['client_id'], ['client.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('account_number')
    )
    op.create_table('card',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('card_number', sa.String(length=16), nullable=False),
    sa.Column('expiration_date', sa.Date(), nullable=False),
    sa.Column('cvv', sa.String(length=3), nullable=False),
    sa.Column('card_type', sa.String(length=20), nullable=False),
    sa.Column('client_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['client_id'], ['client.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('card_number')
    )
    op.create_table('recipient',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=100), nullable=False),
    sa.Column('email', sa.String(length=100), nullable=True),
    sa.Column('account_number', sa.String(length=20), nullable=False),
    sa.Column('phone_number', sa.String(length=15), nullable=True),
    sa.Column('client_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['client_id'], ['client.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('account_number'),
    sa.UniqueConstraint('email'),
    sa.UniqueConstraint('phone_number')
    )
    op.create_table('transaction',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('amount', sa.Float(), nullable=False),
    sa.Column('transaction_type', sa.String(length=10), nullable=False),
    sa.Column('description', sa.String(length=255), nullable=True),
    sa.Column('timestamp', sa.DateTime(), nullable=False),
    sa.Column('account_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['account_id'], ['account.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('transaction')
    op.drop_table('recipient')
    op.drop_table('card')
    op.drop_table('account')
    op.drop_table('client')
    # ### end Alembic commands ###