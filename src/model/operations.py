from datetime import datetime
from decimal import Decimal

from sqlalchemy import Identity, ForeignKey, Text, Numeric, DateTime, func, CheckConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from model.Base import Base
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from model.suppliers import Supplier
    from model.parts import Part
    from model.repair_requests import RepairRequest
    from model.users import User

class Operations(Base):
    __tablename__ = 'operations'

    operation_id: Mapped[int] = mapped_column(Identity(always = True), primary_key = True)
    user_id: Mapped[int] = mapped_column(ForeignKey('users.user_id' , name ='fk_operation_user') ,nullable = False)
    supplier_id: Mapped[int | None] = mapped_column(ForeignKey('suppliers.supplier_id', name ='fk_operation_supplier'),nullable = True)
    part_id: Mapped[int] = mapped_column(ForeignKey('parts.part_id' , name ='fk_operation_part') ,nullable = False)
    request_id: Mapped[int | None] = mapped_column(ForeignKey('repair_requests.request_id', name ='fk_operation_request'),nullable = True)
    type: Mapped[str] = mapped_column(Text, nullable = False)
    quantity: Mapped[int] = mapped_column(nullable = False)
    price: Mapped[Decimal| None ] = mapped_column(Numeric(10,2),nullable = True)
    reason: Mapped[str | None] = mapped_column(Text, nullable = True)
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now() ,nullable = False)

    part: Mapped["Part"] = relationship(back_populates="operations" , lazy = 'raise')
    user: Mapped["User"] = relationship(back_populates="operations" , lazy = 'raise')
    supplier: Mapped["Supplier | None"] = relationship(back_populates="operations", lazy = 'raise')
    request: Mapped["RepairRequest | None"] = relationship(back_populates="operations", lazy = 'raise')

    __table_args__ = (
        CheckConstraint("price >= 0" , name = 'operations_price_check'),
        CheckConstraint("quantity > 0" , name = 'operations_quantity_check'),
        CheckConstraint("type IN ('receipt', 'reserve', 'issue', 'unreserve', 'write_off')", name = 'operations_type_check')
    )