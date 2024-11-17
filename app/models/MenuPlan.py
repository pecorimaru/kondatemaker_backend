from __future__ import annotations
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.orm import Mapped

from typing import TYPE_CHECKING

from app.db.base import Base

# 自身が参照先となっているリレーションは実行時にインポート
if TYPE_CHECKING:
    from app.models.User import User
from app.models.MenuPlanDet import MenuPlanDet


class MenuPlan(Base):
    __tablename__ = 't_menu_plan'

    menu_plan_id = Column(Integer, primary_key=True, nullable=False)
    menu_plan_nm = Column(String, nullable=False)
    menu_plan_nm_k = Column(String, nullable=True)
    owner_user_id = Column(Integer, ForeignKey('m_user.user_id'), nullable=False)
    visibility_flg = Column(String, nullable=True)
    crt_at = Column(String, nullable=True)
    upd_at = Column(String, nullable=True)
    crt_by = Column(String, nullable=True)
    upd_by = Column(String, nullable=True)
    version = Column(Integer, nullable=True)

    rel_m_user: Mapped[User] = relationship("User", back_populates="rel_t_menu_plan")
    rel_t_menu_plan_det: Mapped[list[MenuPlanDet]] = relationship("MenuPlanDet", back_populates="rel_t_menu_plan")
