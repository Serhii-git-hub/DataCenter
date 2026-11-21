
from sqlalchemy import Identity, Text
from sqlalchemy.orm import mapped_column, Mapped, relationship

from model.Base import Base
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from model.operations import Operations

class Supplier(Base):
    __tablename__ = 'suppliers'

    supplier_id: Mapped[int] = mapped_column(Identity(always=True), primary_key=True)
    name: Mapped[str] = mapped_column(Text, nullable=False)
    contact: Mapped[str | None] = mapped_column(Text, nullable=True)

    operations: Mapped[list["Operations"]] = relationship(back_populates="supplier", lazy = 'raise')