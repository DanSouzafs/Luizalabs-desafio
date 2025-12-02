import sqlalchemy as sa

from src.database import metadata

users = sa.Table(
    "users",
    metadata,
    sa.Column("id", sa.Integer, primary_key=True),
    sa.Column("username", sa.String(100), nullable=False, unique=True),
    sa.Column("email", sa.String(255), nullable=False, unique=True),
    sa.Column("hashed_password", sa.String(255), nullable=False),
    sa.Column("created_at", sa.TIMESTAMP(timezone=True), default=sa.func.now()),
)

