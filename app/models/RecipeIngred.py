from __future__ import annotations
from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.orm import Mapped

from typing import TYPE_CHECKING

from app.db.base import Base


if TYPE_CHECKING:
    from app.models.Recipe import Recipe
    from app.models.Ingred import Ingred


class RecipeIngred(Base):
    __tablename__ = 't_recipe_ingred'

    recipe_ingred_id = Column(Integer, primary_key=True, nullable=False)
    recipe_id = Column(Integer, ForeignKey('t_recipe.recipe_id'), nullable=False)
    ingred_id = Column(Integer, ForeignKey('m_ingred.ingred_id'), nullable=False)
    qty = Column(Float, nullable=False)
    unit_cd = Column(String, nullable=False)
    crt_at = Column(String, nullable=True)
    upd_at = Column(String, nullable=True)
    crt_by = Column(String, nullable=True)
    upd_by = Column(String, nullable=True)
    version = Column(Integer, nullable=True)

    rel_t_recipe: Mapped[Recipe] = relationship("Recipe", back_populates="rel_t_recipe_ingred")
    rel_m_ingred: Mapped[Ingred] = relationship("Ingred", back_populates="rel_t_recipe_ingred")
