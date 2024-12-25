from __future__ import annotations
from sqlalchemy import Column, Integer, String, Numeric, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.orm import Mapped

from typing import TYPE_CHECKING

from app.core.base import Base

if TYPE_CHECKING:
    from app.models.User import User


class BuyIngred(Base):
    __tablename__ = 'w_buy_ingred'

    buy_ingred_id = Column(Integer, primary_key=True, autoincrement=True)
    owner_user_id = Column(Integer, ForeignKey('m_user.user_id'), nullable=False)
    ingred_nm = Column(String(80), nullable=False)
    qty = Column(Numeric(8, 2))
    unit_cd = Column(String(2))
    sales_area_type = Column(String(2))
    sales_area_seq = Column(Integer)
    manual_add_flg = Column(String(1))
    bought_flg = Column(String(1))
    fix_buy_flg = Column(String(1))

    rel_m_user: Mapped[User] = relationship("User", foreign_keys=[owner_user_id], back_populates="rel_w_buy_ingred")

