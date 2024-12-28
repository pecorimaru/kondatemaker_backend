from __future__ import annotations
from sqlalchemy import Column, Integer, String, ForeignKey, UniqueConstraint, TIMESTAMP, text
from sqlalchemy.orm import relationship
from sqlalchemy.orm import Mapped

from typing import TYPE_CHECKING

from app.core.base import Base

if TYPE_CHECKING:
    from app.models import User

# 自身が参照先となっているリレーションは実行時にインポート
from app.models import IngredUnitConv
from app.models import RecipeIngred


class Ingred(Base):
    __tablename__ = 'm_ingred'

    ingred_id = Column(Integer, primary_key=True, autoincrement=True)
    ingred_nm = Column(String(80), nullable=False)
    ingred_nm_k = Column(String(160))
    parent_ingred_nm = Column(String(80), nullable=False)
    buy_unit_cd = Column(String(2), nullable=False)
    sales_area_type = Column(String(2), nullable=False)
    owner_user_id = Column(Integer, ForeignKey('m_user.user_id'), nullable=False)
    crt_user_id = Column(Integer, ForeignKey("m_user.user_id"), nullable=False)
    crt_timestamp = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text("now()"))
    upd_user_id = Column(Integer, ForeignKey("m_user.user_id"), nullable=False)
    upd_timestamp = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text("now()"))
    version = Column(Integer, nullable=False, default=0, server_default=text("0"))

    __table_args__ = (
        UniqueConstraint("ingred_nm", "owner_user_id", name="ak1_ingred_nm_owner_user_id"),
    )

    rel_m_user: Mapped[User] = relationship("User", foreign_keys=[owner_user_id], back_populates="rel_m_ingred")
    rel_m_ingred_unit_conv: Mapped[list[IngredUnitConv]] = relationship("IngredUnitConv", back_populates="rel_m_ingred")
    rel_t_recipe_ingred: Mapped[list[RecipeIngred]] = relationship("RecipeIngred", back_populates="rel_m_ingred")
    