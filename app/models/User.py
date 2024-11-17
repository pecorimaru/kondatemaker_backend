from __future__ import annotations
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from sqlalchemy.orm import Mapped

from typing import TYPE_CHECKING

from app.db.base import Base
# 自身が参照先となっているリレーションは実行時にインポート（全て）
from app.models.UserConfig import UserConfig
from app.models.UserGroupRel import UserGroupRel
from app.models.Group import Group
from app.models.Recipe import Recipe
from app.models.MenuPlan import MenuPlan
from app.models.Ingred import Ingred
from app.models.IngredUnitConv import IngredUnitConv
from app.models.BuyIngred import BuyIngred
from app.models.ToweekMenuPlanDet import ToweekMenuPlanDet


class User(Base):
    __tablename__ = 'm_user'

    user_id = Column(Integer, primary_key=True, nullable=False)
    user_nm = Column(String, nullable=False)
    mail_addr = Column(String, nullable=False)
    password = Column(String, nullable=False)
    crt_at = Column(String, nullable=True)
    upd_at = Column(String, nullable=True)
    crt_by = Column(String, nullable=True)
    upd_by = Column(String, nullable=True)
    version = Column(Integer, nullable=True)

    rel_m_user_config: Mapped[list[UserConfig]] = relationship("UserConfig", back_populates="rel_m_user")
    rel_t_user_group_rel: Mapped[list[UserGroupRel]] = relationship("UserGroupRel", back_populates="rel_m_user")
    rel_m_group: Mapped[list[Group]] = relationship("Group", back_populates="rel_m_user")
    rel_t_recipe: Mapped[list[Recipe]] = relationship("Recipe", back_populates="rel_m_user")
    rel_t_menu_plan: Mapped[list[MenuPlan]] = relationship("MenuPlan", back_populates="rel_m_user")
    rel_m_ingred: Mapped[list[Ingred]] = relationship("Ingred", back_populates="rel_m_user")
    rel_m_ingred_unit_conv: Mapped[list[IngredUnitConv]] = relationship("IngredUnitConv", back_populates="rel_m_user")
    rel_w_buy_ingred: Mapped[list[BuyIngred]] = relationship("BuyIngred", back_populates="rel_m_user")
    rel_w_toweek_menu_plan_det: Mapped[list[ToweekMenuPlanDet]] = relationship("ToweekMenuPlanDet", back_populates="rel_m_user")
