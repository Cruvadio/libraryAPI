from datetime import date
from sqlalchemy.ext.asyncio import AsyncAttrs
from pydantic import BaseModel, Field
from typing import Optional
class AuthorAddSchema(BaseModel):
    first_name: Optional[str] = Field(None, description="Имя автора")
    last_name: Optional[str] = Field(None, description="Фамилия автора")
    date_of_birth: Optional[date] = Field(None, description="Дата рождения автора в формате ГГГГ-ММ-ДД")

class AuthorSchema(AuthorAddSchema):
        id: int



class BookAddSchema(BaseModel):
    title: Optional[str] = Field(None, description="Название книги")
    description: Optional[str] = Field(None, description="Описание книги")
    author_id: Optional[int] = Field(None, description="ID автора книги")
    count: Optional[int] = Field(None, ge=0, description="Количество экземпляров книги")
class BookSchema(BookAddSchema):
        id: int

class BorrowAddSchema(BaseModel):
    book_id: Optional[int] = Field(None, description="ID книги, которую взяли")
    name: Optional[str] = Field(None, description="Имя забирающего книгу")
    borrow_date: Optional[date] = Field(None, description="Дата, когда забрали книгу в формате ГГГГ-ММ-ДД")
    return_date: Optional[date] = Field(None, description="Дата, когда забрали книгу в формате ГГГГ-ММ-ДД")
class BorrowSchema(BorrowAddSchema):
        id: int
