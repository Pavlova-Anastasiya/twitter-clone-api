from __future__ import annotations
from datetime import datetime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Integer, Text, DateTime, ForeignKey
from .. import db


class Tweet(db.Model):
__tablename__ = "tweets"


id: Mapped[int] = mapped_column(Integer, primary_key=True)
content: Mapped[str] = mapped_column(Text, nullable=False)
created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)
author_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), nullable=False)


author = relationship("User", back_populates="tweets")
likes = relationship("Like", back_populates="tweet", cascade="all, delete-orphan")
media_items = relationship("Media", back_populates="tweet")