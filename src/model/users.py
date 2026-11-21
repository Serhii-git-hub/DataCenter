
from sqlalchemy import Identity, Text, CheckConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from model.Base import Base
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from model.operations import Operations

class User(Base):
    __tablename__ = "users"

    user_id: Mapped[int] = mapped_column(Identity(always=True), primary_key=True)
    full_name: Mapped[str] = mapped_column(Text , nullable=False)
    login: Mapped[str] = mapped_column(Text , nullable=False, unique=True)
    password_hash: Mapped[str] = mapped_column(Text , nullable=False)
    role: Mapped[str] = mapped_column(Text, nullable= False)

    operations: Mapped[list["Operations"]] = relationship(back_populates='user', lazy = 'raise')

    __table_args__ = (CheckConstraint("role IN ('admin', 'master', 'storekeeper') ", name = 'users_role_check'),)