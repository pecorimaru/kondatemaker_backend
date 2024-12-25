from __future__ import annotations
from sqlalchemy import Column, Integer, String, ForeignKey, UniqueConstraint, TIMESTAMP, text
from sqlalchemy.orm import relationship
from sqlalchemy.orm import Mapped

from typing import TYPE_CHECKING

from app.core.base import Base

# 自身が参照先となっているリレーションは実行時にインポート
if TYPE_CHECKING:
    from app.models.User import User
from app.models.MenuPlanDet import MenuPlanDet


class MenuPlan(Base):
    __tablename__ = 't_menu_plan'

    menu_plan_id = Column(Integer, primary_key=True, autoincrement=True)
    menu_plan_nm = Column(String(80), nullable=False)
    menu_plan_nm_k = Column(String(160))
    owner_user_id = Column(Integer, ForeignKey('m_user.user_id'), nullable=False)
    crt_user_id = Column(Integer, ForeignKey("m_user.user_id"), nullable=False)
    crt_timestamp = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text("now()"))
    upd_user_id = Column(Integer, ForeignKey("m_user.user_id"), nullable=False)
    upd_timestamp = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text("now()"))
    version = Column(Integer, nullable=False, default=0, server_default=text("0"))

    __table_args__ = (
        UniqueConstraint("menu_plan_nm", "owner_user_id", name="ak1_menu_plan_nm_owner_user_id"),
    )

    rel_m_user: Mapped[User] = relationship("User", foreign_keys=[owner_user_id], back_populates="rel_t_menu_plan")
    rel_t_menu_plan_det: Mapped[list[MenuPlanDet]] = relationship("MenuPlanDet", back_populates="rel_t_menu_plan")
