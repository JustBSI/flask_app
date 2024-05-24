from dataclasses import dataclass
from datetime import datetime

from sqlalchemy import DateTime, func
from sqlalchemy.orm import mapped_column, Mapped, DeclarativeBase


class Base(DeclarativeBase):
    pass


@dataclass
class File(Base):
    __tablename__ = 'file'

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    name: Mapped[str] = mapped_column(nullable=False)
    extension: Mapped[str] = mapped_column(nullable=False)
    size: Mapped[int] = mapped_column(nullable=False)
    path: Mapped[str] = mapped_column(nullable=False)
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True),
                                                 nullable=False,
                                                 server_default=func.now())
    updated_at: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), default=None
    )
    comment: Mapped[str | None] = mapped_column(default=None)

    def __repr__(self) -> str:
        return (f'id={self.id!r},'
                f'name={self.name!r},'
                f'extension={self.extension!r},'
                f'size={self.size!r},'
                f'path={self.path!r},'
                f'created_at={self.created_at!r},'
                f'edited_at={self.updated_at!r},'
                f'comment={self.comment!r}')
