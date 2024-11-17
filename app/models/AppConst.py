from __future__ import annotations

from sqlalchemy import Column, Integer, String

from app.db.base import Base


class AppConst(Base):
    __tablename__ = 'c_app_const'

    const_id = Column(Integer, primary_key=True, nullable=False)
    type_cd = Column(String, nullable=False)
    type_nm = Column(String, nullable=True)
    val = Column(String, nullable=True)
    val_content = Column(String, nullable=True)
    sort_seq = Column(Integer, nullable=True)
    generic_item1 = Column(String, nullable=True)
    generic_item2 = Column(String, nullable=True)
    crt_at = Column(String, nullable=True)
    upd_at = Column(String, nullable=True)
    crt_by = Column(String, nullable=True)
    upd_by = Column(String, nullable=True)
    version = Column(Integer, nullable=True)
