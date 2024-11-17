from __future__ import annotations
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.orm import Mapped

from typing import TYPE_CHECKING

from app.db.base import Base

# 自身が参照先となっているリレーションは実行時にインポート
if TYPE_CHECKING:
    from app.models.User import User
from app.models.UserGroupRel import UserGroupRel


class Group(Base):
    __tablename__ = 'm_group'

    group_id = Column(Integer, primary_key=True, nullable=False)
    group_nm = Column(String, nullable=False)
    owner_user_id = Column(Integer, ForeignKey('m_user.user_id'), nullable=False)
    crt_at = Column(String, nullable=True)
    upd_at = Column(String, nullable=True)
    crt_by = Column(String, nullable=True)
    upd_by = Column(String, nullable=True)
    version = Column(Integer, nullable=True)

    rel_t_user_group_rel: Mapped[list[UserGroupRel]] = relationship("UserGroupRel", back_populates="rel_m_group")
    rel_m_user: Mapped[User] = relationship("User", back_populates="rel_m_group")

