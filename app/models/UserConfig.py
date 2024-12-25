from __future__ import annotations
from sqlalchemy import Column, Integer, String, ForeignKey, UniqueConstraint, TIMESTAMP, text
from sqlalchemy.orm import relationship
from sqlalchemy.orm import Mapped

from typing import TYPE_CHECKING

from app.core.base import Base

if TYPE_CHECKING:
    from app.models.User import User


class UserConfig(Base):
    __tablename__ = 'm_user_config'

    user_config_id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey('m_user.user_id'), nullable=False)
    config_type = Column(String(2), nullable=False)
    val = Column(String(2))
    crt_user_id = Column(Integer, ForeignKey("m_user.user_id"), nullable=False)
    crt_timestamp = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text("now()"))
    upd_user_id = Column(Integer, ForeignKey("m_user.user_id"), nullable=False)
    upd_timestamp = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text("now()"))
    version = Column(Integer, nullable=False, default=0, server_default=text("0"))

    __table_args__ = (
        UniqueConstraint("user_id", "config_type", name="ak1_user_id_config_type"),
    )

    rel_m_user: Mapped[User] = relationship("User", foreign_keys=[user_id], back_populates="rel_m_user_config")