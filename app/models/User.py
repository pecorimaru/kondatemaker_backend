from __future__ import annotations
from sqlalchemy import Column, Integer, String, ForeignKey, TIMESTAMP, text
from sqlalchemy.orm import relationship
from sqlalchemy.orm import Mapped

from typing import TYPE_CHECKING

from app.core.base import Base
# 自身が参照先となっているリレーションは実行時にインポート（全て）
from app.models.UserConfig import UserConfig
from app.models.GroupConfig import GroupConfig
from app.models.Group import Group
from app.models.Recipe import Recipe
from app.models.MenuPlan import MenuPlan
from app.models.Ingred import Ingred
from app.models.BuyIngred import BuyIngred
from app.models.ToweekMenuPlanDet import ToweekMenuPlanDet


class User(Base):
    __tablename__ = 'm_user'

    user_id = Column(Integer, primary_key=True, autoincrement=True)
    user_nm = Column(String(80))
    email_addr = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    dele_flg = Column(String(1))
    crt_user_id = Column(Integer, ForeignKey("m_user.user_id"), nullable=False)
    crt_timestamp = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text("now()"))
    upd_user_id = Column(Integer, ForeignKey("m_user.user_id"), nullable=False)
    upd_timestamp = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text("now()"))
    version = Column(Integer, nullable=False, default=0, server_default=text("0"))

    rel_m_user_config: Mapped[list[UserConfig]] = relationship("UserConfig", foreign_keys="UserConfig.user_id", back_populates="rel_m_user")
    rel_m_group: Mapped[list[Group]] = relationship("Group", foreign_keys="Group.owner_user_id", back_populates="rel_m_user")
    rel_m_group_config: Mapped[list[GroupConfig]] = relationship("GroupConfig", foreign_keys="GroupConfig.user_id", back_populates="rel_m_user")
    rel_t_recipe: Mapped[list[Recipe]] = relationship("Recipe", foreign_keys="Recipe.owner_user_id", back_populates="rel_m_user")
    rel_t_menu_plan: Mapped[list[MenuPlan]] = relationship("MenuPlan", foreign_keys="MenuPlan.owner_user_id", back_populates="rel_m_user")
    rel_m_ingred: Mapped[list[Ingred]] = relationship("Ingred", foreign_keys="Ingred.owner_user_id", back_populates="rel_m_user")
    # rel_m_ingred_unit_conv: Mapped[list[IngredUnitConv]] = relationship("IngredUnitConv", back_populates="rel_m_user")
    rel_w_buy_ingred: Mapped[list[BuyIngred]] = relationship("BuyIngred", foreign_keys="BuyIngred.owner_user_id", back_populates="rel_m_user")
    rel_w_toweek_menu_plan_det: Mapped[list[ToweekMenuPlanDet]] = relationship("ToweekMenuPlanDet", foreign_keys="ToweekMenuPlanDet.owner_user_id", back_populates="rel_m_user")
