from __future__ import annotations
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.orm import Mapped

from typing import TYPE_CHECKING

from app.db.base import Base


if TYPE_CHECKING:
    from app.models.MenuPlan import MenuPlan
    from app.models.Recipe import Recipe


class MenuPlanDet(Base):
    __tablename__ = 't_menu_plan_det'

    menu_plan_det_id = Column(Integer, primary_key=True, nullable=False)
    menu_plan_id = Column(Integer, ForeignKey('t_menu_plan.menu_plan_id'), nullable=False)
    week_day_cd = Column(String, nullable=False)
    recipe_id = Column(Integer, ForeignKey('t_recipe.recipe_id'), nullable=True)
    crt_at = Column(String, nullable=True)
    upd_at = Column(String, nullable=True)
    crt_by = Column(String, nullable=True)
    upd_by = Column(String, nullable=True)
    version = Column(Integer, nullable=True)

    rel_t_menu_plan: Mapped[MenuPlan] = relationship("MenuPlan", back_populates="rel_t_menu_plan_det")
    rel_t_recipe: Mapped[Recipe] = relationship("Recipe", back_populates="rel_t_menu_plan_det")
