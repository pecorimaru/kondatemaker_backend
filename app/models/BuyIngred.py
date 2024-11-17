from __future__ import annotations
from sqlalchemy import Column, Integer, String, REAL, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.orm import Mapped

from typing import TYPE_CHECKING

from app.db.base import Base

if TYPE_CHECKING:
    from app.models.User import User


class BuyIngred(Base):
    __tablename__ = 'w_buy_ingred'

    buy_ingred_id = Column(Integer, primary_key=True, nullable=False)
    user_id = Column(Integer, ForeignKey('m_user.user_id'), nullable=False)
    ingred_nm = Column(String, nullable=False)
    qty = Column(REAL, nullable=True)
    unit_cd = Column(String, nullable=True)
    sales_area_type = Column(String, nullable=True)
    sales_area_seq = Column(Integer, nullable=True)
    manual_add_flg = Column(String, nullable=True)
    bought_flg = Column(String, nullable=True)

    rel_m_user: Mapped[User] = relationship("User", back_populates="rel_w_buy_ingred") # type: ignore
    # rel_m_ingred: Mapped[Ingred] = relationship("Ingred", back_populates="rel_w_buy_ingred") # type: ignore

