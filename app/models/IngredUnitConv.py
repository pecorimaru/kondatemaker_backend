from __future__ import annotations
from sqlalchemy import Column, Integer, String, Numeric, ForeignKey, UniqueConstraint, TIMESTAMP, text
from sqlalchemy.orm import relationship
from sqlalchemy.orm import Mapped

from typing import TYPE_CHECKING

from app.core.base import Base

if TYPE_CHECKING:
    from app.models.Ingred import Ingred
    from app.models.User import User


class IngredUnitConv(Base):
    __tablename__ = 'm_ingred_unit_conv'

    ingred_unit_conv_id = Column(Integer, primary_key=True, autoincrement=True)
    ingred_id = Column(Integer, ForeignKey('m_ingred.ingred_id'), nullable=False)
    conv_unit_cd = Column(String(2), nullable=False)
    conv_rate = Column(Numeric(8, 4), nullable=False)
    crt_user_id = Column(Integer, ForeignKey("m_user.user_id"), nullable=False)
    crt_timestamp = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text("now()"))
    upd_user_id = Column(Integer, ForeignKey("m_user.user_id"), nullable=False)
    upd_timestamp = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text("now()"))
    version = Column(Integer, nullable=False, default=0, server_default=text("0"))

    __table_args__ = (
        UniqueConstraint("ingred_id", "conv_unit_cd", name="ak1_ingred_id_conv_unit_cd"),
    )

    rel_m_ingred: Mapped[Ingred] = relationship("Ingred", back_populates="rel_m_ingred_unit_conv")

