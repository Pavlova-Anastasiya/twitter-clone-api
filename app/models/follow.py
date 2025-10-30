from __future__ import annotations
from datetime import datetime
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Integer, DateTime, ForeignKey, UniqueConstraint
from .. import db


class Follow(db.Model):
__tablename__ = "follows"
__table_args__ = (UniqueConstraint("follower_id", "following_id", name="uq_follow_rel"),)


id: Mapped[int] = mapped_column(Integer, primary_key=True)
follower_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
following_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow, nullable=False)


follower = relationship("User", foreign_keys=[follower_id], back_populates="following")
following = relationship("User", foreign_keys=[following_id], back_populates="followers")