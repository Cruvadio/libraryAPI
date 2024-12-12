from .database import Base
from datetime import date
from sqlalchemy import Integer, String, Date, ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.ext.asyncio import AsyncAttrs
from pydantic import BaseModel, Field
from typing import Optional
class Author(Base):
    first_name: Mapped[str]
    last_name: Mapped[str]
    date_of_birth: Mapped[date]
    books: Mapped[list["Book"]] = relationship(
        "Book",
        back_populates="author",
        cascade="all, delete-orphan"
    )


    def to_dict(self):
        return {
            "id": self.id,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "date_of_birth": self.date_of_birth
        }

class Book(Base):
    title: Mapped[str]
    description: Mapped[str]
    author_id: Mapped[int] = mapped_column(ForeignKey('authors.id'))
    count: Mapped[int] = mapped_column(default=0)
    author: Mapped["Author"] = relationship(
        "Author",
        back_populates="books"
    )
    borrows: Mapped["Borrow"] = relationship(
        "Borrow",
        back_populates="book",
        cascade="all, delete-orphan"
    )


class Borrow(Base):
    book_id: Mapped[int] = mapped_column(ForeignKey('books.id'))
    name: Mapped[str]
    borrow_date: Mapped[date] = mapped_column(server_default=func.current_date())
    return_date: Mapped[date | None]
    book: Mapped["Book"] = relationship(
        "Book",
        back_populates="borrows"
    )

