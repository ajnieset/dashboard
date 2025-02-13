from advanced_alchemy.base import BigIntAuditBase
from sqlalchemy.orm import Mapped, mapped_column


class User(BigIntAuditBase):
    __tablename__ = "user"

    email: Mapped[str] = mapped_column(unique=True)
    name: Mapped[str]
    password_hash: Mapped[str]
