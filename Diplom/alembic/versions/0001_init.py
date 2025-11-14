'''
Начальная миграция.

Создаёт таблицы:
- users (id, name, api_key уникальный);
- tweets (id, author_id FK, content, created_at);
- medias (id, path, created_at);
- tweet_medias (tweet_id, media_id);
- likes (user_id, tweet_id, PK составной);
- follows (follower_id, followee_id, PK составной).
'''
from __future__ import annotations

from alembic import op
import sqlalchemy as sa

revision = "0001_init"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "users",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("name", sa.String(120), nullable=False),
        sa.Column("api_key", sa.String(255), unique=True, nullable=False, index=True),
    )

    op.create_table(
        "tweets",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("author_id", sa.Integer, sa.ForeignKey("users.id", ondelete="CASCADE"), nullable=False),
        sa.Column("content", sa.Text, nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("NOW()"), nullable=False),
    )

    op.create_table(
        "medias",
        sa.Column("id", sa.Integer, primary_key=True),
        sa.Column("path", sa.String(512), nullable=False),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("NOW()"), nullable=False),
    )

    op.create_table(
        "tweet_medias",
        sa.Column("tweet_id", sa.Integer, sa.ForeignKey("tweets.id", ondelete="CASCADE"), primary_key=True),
        sa.Column("media_id", sa.Integer, sa.ForeignKey("medias.id", ondelete="CASCADE"), primary_key=True),
    )

    op.create_table(
        "likes",
        sa.Column("user_id", sa.Integer, sa.ForeignKey("users.id", ondelete="CASCADE"), primary_key=True),
        sa.Column("tweet_id", sa.Integer, sa.ForeignKey("tweets.id", ondelete="CASCADE"), primary_key=True),
        sa.Column("created_at", sa.DateTime(timezone=True), server_default=sa.text("NOW()"), nullable=False),
    )

    op.create_table(
        "follows",
        sa.Column("follower_id", sa.Integer, sa.ForeignKey("users.id", ondelete="CASCADE"), primary_key=True),
        sa.Column("followee_id", sa.Integer, sa.ForeignKey("users.id", ondelete="CASCADE"), primary_key=True),
        sa.CheckConstraint("follower_id <> followee_id", name="no_self_follow"),
    )


def downgrade() -> None:
    op.drop_table("follows")
    op.drop_table("likes")
    op.drop_table("tweet_medias")
    op.drop_table("medias")
    op.drop_table("tweets")
    op.drop_table("users")
