from __future__ import annotations
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.orm import Mapped

from typing import TYPE_CHECKING

from app.db.base import Base

# 自身が参照先となっているリレーションは実行時にインポート
if TYPE_CHECKING:
    from app.models.User import User
from app.models.RecipeIngred import RecipeIngred
from app.models.MenuPlanDet import MenuPlanDet
from app.models.ToweekMenuPlanDet import ToweekMenuPlanDet


class Recipe(Base):
    __tablename__ = 't_recipe'

    recipe_id = Column(Integer, primary_key=True, nullable=False)
    recipe_nm = Column(String, nullable=False)
    recipe_type = Column(String, nullable=True)
    owner_id = Column(String, ForeignKey('m_user.user_id'), nullable=False)
    recipe_url = Column(String, nullable=True)
    visibility_flg = Column(String, nullable=True)
    crt_at = Column(String, nullable=True)
    upd_at = Column(String, nullable=True)
    crt_by = Column(String, nullable=True)
    upd_by = Column(String, nullable=True)
    version = Column(Integer, nullable=True)
    recipe_nm_k = Column(String, nullable=True)

    rel_m_user: Mapped[User] = relationship("User", back_populates="rel_t_recipe")
    rel_t_recipe_ingred: Mapped[list[RecipeIngred]] = relationship("RecipeIngred", back_populates="rel_t_recipe")
    rel_t_menu_plan_det: Mapped[list[MenuPlanDet]] = relationship("MenuPlanDet", back_populates="rel_t_recipe")
    rel_w_toweek_menu_plan_det: Mapped[list[ToweekMenuPlanDet]] = relationship("ToweekMenuPlanDet", back_populates="rel_t_recipe")
