from sqlalchemy import Identity, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from model.Base import Base
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from model.parts import Part

class Categories(Base):
    __tablename__ = 'categories'

    category_id: Mapped[int] = mapped_column(Identity(always = True), primary_key = True)
    name: Mapped[str] = mapped_column(Text, nullable = False, unique = True)

    parts: Mapped[list["Part"]] = relationship(back_populates='category', lazy = 'raise')