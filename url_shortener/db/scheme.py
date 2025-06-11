from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column


class Base(DeclarativeBase):
    pass


class Urls(Base):
    __tablename__ = "urls"

    id: Mapped[int] = mapped_column(primary_key=True)
    user_url: Mapped[str] = mapped_column(nullable=False)
    short_url: Mapped[str] = mapped_column(nullable=False)

    def __repr__(self):
        return f"<Urls(id={self.id!r}, user_url={self.user_url!r}, short_url={self.short_url!r})>"
