from __future__ import annotations
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.orm import Mapped

from typing import TYPE_CHECKING

from app.db.base import Base

# 自身が参照先となっているリレーションは実行時にインポート
if TYPE_CHECKING:
    from app.models import User
from app.models import IngredUnitConv
from app.models import RecipeIngred


class Ingred(Base):
    __tablename__ = 'm_ingred'

    ingred_id = Column(Integer, primary_key=True, nullable=False)
    ingred_nm = Column(String, nullable=False)
    ingred_nm_k = Column(String, nullable=True)
    parent_ingred_nm = Column(String, nullable=False)
    standard_unit_cd = Column(String, nullable=False)
    sales_area_type = Column(String, nullable=True)
    owner_user_id = Column(Integer, ForeignKey('m_user.user_id'), nullable=False)
    crt_at = Column(String, nullable=True)
    upd_at = Column(String, nullable=True)
    crt_by = Column(String, nullable=True)
    upd_by = Column(String, nullable=True)
    version = Column(Integer, nullable=True)

    rel_m_ingred_unit_conv: Mapped[list[IngredUnitConv]] = relationship("IngredUnitConv", back_populates="rel_m_ingred")
    rel_m_user: Mapped[User] = relationship("User", back_populates="rel_m_ingred")
    rel_t_recipe_ingred: Mapped[list[RecipeIngred]] = relationship("RecipeIngred", back_populates="rel_m_ingred")
    # rel_w_buy_ingred: Mapped[list[BuyIngred]] = relationship("BuyIngred", back_populates="rel_m_ingred")
    