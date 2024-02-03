from datetime import datetime

from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column


class Base(DeclarativeBase):
    pass


class CurrencyCourse(Base):
    __tablename__ = 'currency_courses'

    id: Mapped[int] = mapped_column(primary_key=True)
    exchanger: Mapped[str]
    direction: Mapped[str]
    value: Mapped[float]
    updated_at: Mapped[datetime] = mapped_column(default=datetime.utcnow, onupdate=datetime.utcnow)
