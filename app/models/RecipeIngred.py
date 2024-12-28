from __future__ import annotations
from sqlalchemy import Column, Integer, String, Numeric, ForeignKey, UniqueConstraint, TIMESTAMP, text
from sqlalchemy.orm import relationship
from sqlalchemy.orm import Mapped

from typing import TYPE_CHECKING

from app.core.base import Base


if TYPE_CHECKING:
    from app.models.Recipe import Recipe
    from app.models.Ingred import Ingred


class RecipeIngred(Base):
    __tablename__ = 't_recipe_ingred'

    recipe_ingred_id = Column(Integer, primary_key=True, autoincrement=True)
    recipe_id = Column(Integer, ForeignKey('t_recipe.recipe_id'), nullable=False)
    ingred_id = Column(Integer, ForeignKey('m_ingred.ingred_id'), nullable=False)
    qty = Column(Numeric(8, 2), nullable=False)
    unit_cd = Column(String(2), nullable=False)
    crt_user_id = Column(Integer, ForeignKey("m_user.user_id"), nullable=False)
    crt_timestamp = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text("now()"))
    upd_user_id = Column(Integer, ForeignKey("m_user.user_id"), nullable=False)
    upd_timestamp = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text("now()"))
    version = Column(Integer, nullable=False, default=0, server_default=text("0"))

    __table_args__ = (
        UniqueConstraint("recipe_id", "ingred_id", name="ak1_recipe_id_ingred_id"),
    )

    rel_t_recipe: Mapped[Recipe] = relationship("Recipe", back_populates="rel_t_recipe_ingred")
    rel_m_ingred: Mapped[Ingred] = relationship("Ingred", back_populates="rel_t_recipe_ingred")
