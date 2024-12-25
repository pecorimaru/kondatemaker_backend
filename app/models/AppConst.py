from __future__ import annotations

from sqlalchemy import Column, Integer, String, ForeignKey, UniqueConstraint, TIMESTAMP, text

from app.core.base import Base


class AppConst(Base):
    __tablename__ = 'c_app_const'

    const_id = Column(Integer, primary_key=True, autoincrement=True)
    type_cd = Column(String(5), nullable=False)
    type_nm = Column(String(80))
    val = Column(String(3))
    val_content = Column(String(80))
    sort_seq = Column(Integer)
    generic_item1 = Column(String(80))
    generic_item2 = Column(String(80))
    crt_user_id = Column(Integer, ForeignKey("m_user.user_id"), nullable=False)
    crt_timestamp = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text("now()"))
    upd_user_id = Column(Integer, ForeignKey("m_user.user_id"), nullable=False)
    upd_timestamp = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text("now()"))
    version = Column(Integer, nullable=False, default=0, server_default=text("0"))

    __table_args__ = (
        UniqueConstraint("type_cd", "val", name="ak1_type_cd_val"),
    )