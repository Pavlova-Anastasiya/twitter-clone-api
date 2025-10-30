from __future__ import annotations
from datetime import datetime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Integer, DateTime, ForeignKey, String
from .. import db


class Media(db.Model):
__tablename__ = "media"


id: Mapped[int] = mapped_column(Integer, primary_key=True)
filename: Mapped[str] = mapped_column(String(255), nullable=False)
path: Mapped[str] = mapped_column(String(512), nullable=False)
content_type: Mapped[str] = mapped_column(String(120), nullable=True)
owner_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="SET NULL"), nullable=True)
tweet_id: Mapped[int] = mapped_column(ForeignKey("tweets.id", ondelete="SET NULL"), nullable=True)
created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)


tweet = relationship("Tweet", back_populates="media_items")