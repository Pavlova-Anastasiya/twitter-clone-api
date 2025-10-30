from __future__ import annotations
from datetime import datetime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Integer, DateTime, ForeignKey, UniqueConstraint
from .. import db


class Like(db.Model):
__tablename__ = "likes"
__table_args__ = (UniqueConstraint("user_id", "tweet_id", name="uq_like_user_tweet"),)


id: Mapped[int] = mapped_column(Integer, primary_key=True)
user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
tweet_id: Mapped[int] = mapped_column(ForeignKey("tweets.id", ondelete="CASCADE"), nullable=False)
created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)


user = relationship("User", back_populates="likes")
tweet = relationship("Tweet", back_populates="likes")