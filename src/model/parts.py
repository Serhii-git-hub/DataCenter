from decimal import Decimal
from typing import TYPE_CHECKING
from sqlalchemy import Identity, ForeignKey, Text, CheckConstraint, Numeric
from sqlalchemy.orm import Mapped, mapped_column, relationship

from model.Base import Base
if TYPE_CHECKING:
    from model.categories import Categories
    from model.operations import Operations

class Part(Base):
    __tablename__ = 'parts'
    part_id: Mapped[int] = mapped_column(Identity(always = True), primary_key=True)
    category_id: Mapped[int] = mapped_column(ForeignKey('categories.category_id' , name= 'fk_category_parts'), nullable=False)
    name: Mapped[str] = mapped_column(Text, nullable=False)
    sku: Mapped[str] = mapped_column(Text, nullable=False, unique=True)
    price: Mapped[Decimal] = mapped_column(Numeric(10,2),nullable=False)
    quantity: Mapped[int] = mapped_column(nullable=False, server_default='0')
    reserved: Mapped[int] = mapped_column(nullable=False, server_default='0')
    min_stock: Mapped[int] = mapped_column(nullable=False, server_default='0')

    category: Mapped["Categories"] = relationship(back_populates="parts", lazy="raise")
    operations: Mapped[list["Operations"]] = relationship(back_populates="part", lazy="raise")

    __table_args__ = (
        CheckConstraint('price >= 0' , name = 'parts_price_check'),
        CheckConstraint('quantity >= 0', name = 'parts_quantity_check'),
        CheckConstraint('min_stock >= 0', name = 'parts_min_stock_check'),
        CheckConstraint('reserved >= 0 AND reserved <= quantity', name = 'parts_check')
    )

