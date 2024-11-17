from __future__ import annotations
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.orm import Mapped

from typing import TYPE_CHECKING

from app.db.base import Base

if TYPE_CHECKING:
    from app.models.User import User


class UserConfig(Base):
    __tablename__ = 'm_user_config'

    user_config_id = Column(Integer, primary_key=True, nullable=False)
    user_id = Column(Integer, ForeignKey('m_user.user_id'), nullable=False)
    config_type = Column(String, nullable=False)
    config_val = Column(String, nullable=True)
    crt_at = Column(String, nullable=True)
    upd_at = Column(String, nullable=True)
    crt_by = Column(String, nullable=True)
    upd_by = Column(String, nullable=True)
    version = Column(Integer, nullable=True)

    rel_m_user: Mapped[User] = relationship("User", back_populates="rel_m_user_config")