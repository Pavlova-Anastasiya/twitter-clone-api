from __future__ import annotations
from datetime import datetime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, Integer, DateTime
from .. import db


class User(db.Model):
__tablename__ = "users"


id: Mapped[int] = mapped_column(Integer, primary_key=True)
name: Mapped[str] = mapped_column(String(120), nullable=False)
api_key: Mapped[str] = mapped_column(String(255), unique=True, nullable=False)
created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)


tweets = relationship("Tweet", back_populates="author", cascade="all, delete-orphan")
likes = relationship("Like", back_populates="user", cascade="all, delete-orphan")


following = relationship(
"Follow",
foreign_keys="Follow.follower_id",
back_populates="follower",
cascade="all, delete-orphan",
)
followers = relationship(
"Follow",
foreign_keys="Follow.following_id",
back_populates="following",
cascade="all, delete-orphan",
)


def to_simple(self) -> dict:
return {"id": self.id, "name": self.name}