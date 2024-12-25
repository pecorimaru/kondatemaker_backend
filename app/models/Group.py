from __future__ import annotations
from sqlalchemy import Column, Integer, String, ForeignKey, UniqueConstraint, TIMESTAMP, text
from sqlalchemy.orm import relationship
from sqlalchemy.orm import Mapped

from typing import TYPE_CHECKING

from app.core.base import Base

# 自身が参照先となっているリレーションは実行時にインポート
if TYPE_CHECKING:
    from app.models.User import User
from app.models.GroupConfig import GroupConfig
# from app.models.BuyIngred import BuyIngred
# from app.models.ToweekMenuPlanDet import ToweekMenuPlanDet


class Group(Base):
    __tablename__ = 'm_group'

    group_id = Column(Integer, primary_key=True, autoincrement=True)
    group_nm = Column(String(80), nullable=False)
    owner_user_id = Column(Integer, ForeignKey('m_user.user_id'), nullable=False)
    crt_user_id = Column(Integer, ForeignKey("m_user.user_id"), nullable=False)
    crt_timestamp = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text("now()"))
    upd_user_id = Column(Integer, ForeignKey("m_user.user_id"), nullable=False)
    upd_timestamp = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text("now()"))
    version = Column(Integer, nullable=False, default=0, server_default=text("0"))

    __table_args__ = (
        UniqueConstraint("group_nm", "owner_user_id", name="ak1_group_nm_owner_user_id"),
    )

    rel_m_user: Mapped[User] = relationship("User", foreign_keys=[owner_user_id], back_populates="rel_m_group")
    rel_m_group_config: Mapped[list[GroupConfig]] = relationship("GroupConfig", back_populates="rel_m_group")
    # rel_w_buy_ingred: Mapped[list[BuyIngred]] = relationship("BuyIngred", back_populates="rel_m_group")
    # rel_w_toweek_menu_plan_det: Mapped[list[ToweekMenuPlanDet]] = relationship("ToweekMenuPlanDet", back_populates="rel_m_group")
