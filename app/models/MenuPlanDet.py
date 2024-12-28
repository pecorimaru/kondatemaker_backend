from __future__ import annotations
from sqlalchemy import Column, Integer, String, ForeignKey, TIMESTAMP, text
from sqlalchemy.orm import relationship
from sqlalchemy.orm import Mapped

from typing import TYPE_CHECKING

from app.core.base import Base


if TYPE_CHECKING:
    from app.models.MenuPlan import MenuPlan
    from app.models.Recipe import Recipe


class MenuPlanDet(Base):
    __tablename__ = 't_menu_plan_det'

    menu_plan_det_id = Column(Integer, primary_key=True, autoincrement=True)
    menu_plan_id = Column(Integer, ForeignKey('t_menu_plan.menu_plan_id'), nullable=False)
    weekday_cd = Column(String(1), nullable=False)
    recipe_id = Column(Integer, ForeignKey('t_recipe.recipe_id'), nullable=False)
    crt_user_id = Column(Integer, ForeignKey("m_user.user_id"), nullable=False)
    crt_timestamp = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text("now()"))
    upd_user_id = Column(Integer, ForeignKey("m_user.user_id"), nullable=False)
    upd_timestamp = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text("now()"))
    version = Column(Integer, nullable=False, default=0, server_default=text("0"))

    rel_t_menu_plan: Mapped[MenuPlan] = relationship("MenuPlan", back_populates="rel_t_menu_plan_det")
    rel_t_recipe: Mapped[Recipe] = relationship("Recipe", back_populates="rel_t_menu_plan_det")
