from __future__ import annotations
from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.orm import Mapped

from typing import TYPE_CHECKING

from app.db.base import Base

if TYPE_CHECKING:
    from app.models.Ingred import Ingred
    from app.models.User import User


class IngredUnitConv(Base):
    __tablename__ = 'm_ingred_unit_conv'

    ingred_unit_conv_id = Column(Integer, primary_key=True, nullable=False)
    ingred_id = Column(Integer, ForeignKey('m_ingred.ingred_id'), nullable=False)
    from_unit_cd = Column(String, nullable=False)
    conv_rate = Column(Float, nullable=False)
    owner_user_id = Column(Integer, ForeignKey('m_user.user_id'), nullable=False)
    crt_at = Column(String, nullable=True)
    upd_at = Column(String, nullable=True)
    crt_by = Column(String, nullable=True)
    upd_by = Column(String, nullable=True)
    version = Column(Integer, nullable=True)

    rel_m_ingred: Mapped[Ingred] = relationship("Ingred", back_populates="rel_m_ingred_unit_conv")
    rel_m_user: Mapped[User] = relationship("User", back_populates="rel_m_ingred_unit_conv")

