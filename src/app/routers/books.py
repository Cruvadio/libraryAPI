from app.schemas import BookSchema, BookAddSchema
from app.database import async_session_maker
from app.dao import BoookDAO
from fastapi import APIRouter, status

router_books = APIRouter(prefix='/books', tags=['Работа с книгами'])
@router_books.post("/",summary="Добавление новой книги в базу данных", status_code=status.HTTP_201_CREATED)
async def add_book(book_data: BookAddSchema):
    async with async_session_maker() as session:
        new_book = await BoookDAO.add(session, **book_data.dict())
        return {"message": "Book added successfully", "book": new_book}

@router_books.get("/", summary="Получить список всех книг", response_model=list[BookSchema])
async def get_books()-> list[BookSchema]:
    async with async_session_maker() as session:
        authors = await BoookDAO.find_all(session)
    return authors

@router_books.get("/{id}", summary="Получить одну книгу по id")
async def get_book_by_id(id: int) -> BookSchema:
    async with async_session_maker() as session:
        return await BoookDAO.find_one_or_none_by_id(session=session, data_id=id)

@router_books.put("/{id}", summary="Изменить одну книгу по id")
async def update_book_info(id: int, author_data: BookAddSchema) -> BookSchema:
    async with async_session_maker() as session:
        return await BoookDAO.update_one_by_id(session=session, data_id=id, values=author_data)

@router_books.delete("/{id}", summary="Удалить одну книгу по id")
async def delete_book(id: int):
    async with async_session_maker() as session:
        await BoookDAO.delete_one_by_id(session=session, data_id=id)
        return {"message": "Book removed successfully"}
