from __future__ import annotations
from sqlalchemy import Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.orm import Mapped

from typing import TYPE_CHECKING

from app.core.base import Base

if TYPE_CHECKING:
    from app.models.User import User
    from app.models.Recipe import Recipe


class ToweekMenuPlanDet(Base):
    __tablename__ = 'w_toweek_menu_plan_det'

    toweek_menu_plan_det_id = Column(Integer, primary_key=True, autoincrement=True)
    owner_user_id = Column(Integer, ForeignKey('m_user.user_id'), nullable=False)
    weekday_cd = Column(String, nullable=False)
    recipe_id = Column(Integer, ForeignKey('t_recipe.recipe_id'))
    crt_dt = Column(Date)

    rel_m_user: Mapped[User] = relationship("User", foreign_keys=[owner_user_id], back_populates="rel_w_toweek_menu_plan_det")
    rel_t_recipe: Mapped[Recipe] = relationship("Recipe", back_populates="rel_w_toweek_menu_plan_det")
