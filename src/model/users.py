from sqlalchemy.orm import Mapped, mapped_column


class User():
    __tablename__ = "users"

    id: Mapped[int] = mapped_column()