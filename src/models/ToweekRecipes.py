from __future__ import annotations
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.orm import Mapped

from src.db.base import Base
# from models.models import User
# from models.models import Recipe

class ToweekRecipes(Base):
    __tablename__ = 'w_toweek_recipes'

    toweek_recipes_id = Column(Integer, primary_key=True, nullable=False)
    user_id = Column(Integer, ForeignKey('m_user.user_id'), nullable=False)
    weekday_cd = Column(String, nullable=False)
    recipe_id = Column(Integer, ForeignKey('t_recipe.recipe_id'), nullable=True)
    crt_dt = Column(String, nullable=True)

    rel_m_user: Mapped[User] = relationship("User", back_populates="rel_w_toweek_recipes") # type: ignore
    rel_t_recipe: Mapped[Recipe] = relationship("Recipe", back_populates="rel_w_toweek_recipes") # type: ignore
