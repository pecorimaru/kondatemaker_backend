from __future__ import annotations
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.orm import Mapped

from typing import TYPE_CHECKING

from app.db.base import Base

if TYPE_CHECKING:
    from app.models.User import User
    from app.models.Group import Group


class UserGroupRel(Base):
    __tablename__ = 't_user_group_rel'

    user_group_rel_id = Column(Integer, primary_key=True, nullable=False)
    user_id = Column(Integer, ForeignKey('m_user.user_id'), nullable=False)
    group_id = Column(Integer, ForeignKey('m_group.group_id'), nullable=False)
    crt_at = Column(String, nullable=True)
    upd_at = Column(String, nullable=True)
    crt_by = Column(String, nullable=True)
    upd_by = Column(String, nullable=True)
    version = Column(Integer, nullable=True)

    rel_m_user: Mapped[User] = relationship("User", back_populates="rel_t_user_group_rel")
    rel_m_group: Mapped[Group] = relationship("Group", back_populates="rel_t_user_group_rel")
