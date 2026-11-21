from datetime import datetime

from sqlalchemy import Identity, ForeignKey, Text, DateTime, func, CheckConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from model.Base import Base
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from model.operations import Operations

class RepairRequest(Base):
    __tablename__ = 'repair_requests'

    request_id: Mapped[int] = mapped_column(Identity(always = True), primary_key = True)
    user_id: Mapped[int] = mapped_column(ForeignKey('users.user_id' , name = 'fk_repair_req_user'), nullable = False)
    client_name: Mapped[str] = mapped_column(Text, nullable = False)
    phone: Mapped[str] = mapped_column(Text, nullable = False)
    device: Mapped[str] = mapped_column(Text, nullable = False)
    fault_description: Mapped[str] = mapped_column(Text, nullable = False)
    status: Mapped[str] = mapped_column(Text, nullable = False, default='diagnostic')
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now() ,nullable = False)

    operations: Mapped[list["Operations"]] = relationship(back_populates="request", lazy = 'raise')
    __table_args__ = (
        CheckConstraint("status IN ('diagnostic', 'done', 'in_process', 'waiting_parts', 'issued')", name='repair_requests_status_check'),
    )