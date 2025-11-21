"""
ORM-модель подписок (кто на кого подписан).
"""
from __future__ import annotations

from sqlalchemy import CheckConstraint, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from app.models.base import Base


class Follow(Base):
    """
    Подписка: follower -> followee (составной PK).

    Ограничения:
        - запрет самоподписки (CheckConstraint).
    """
    __tablename__ = "follows"

    follower_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), primary_key=True)
    followee_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), primary_key=True)

    __table_args__ = (
        CheckConstraint("follower_id <> followee_id", name="no_self_follow"),
    )
