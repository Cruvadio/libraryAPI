from app.schemas import AuthorSchema, AuthorAddSchema
from app.database import async_session_maker
from app.dao import AuthorDAO
from fastapi import APIRouter, status


router_authors = APIRouter(prefix='/authors', tags=['Работа с авторами'])
@router_authors.post("/", summary="Добавление нового автора в базу данных.", status_code=status.HTTP_201_CREATED)
async def add_author(author_data: AuthorAddSchema):
    async with async_session_maker() as session:
        new_author = await AuthorDAO.add(session, **author_data.dict())
        return {"message": "Author added successfully", "author": new_author}

@router_authors.get("/", summary="Получить всех авторов", response_model=list[AuthorSchema])
async def get_authors()-> list[AuthorSchema]:
    async with async_session_maker() as session:
        authors = await AuthorDAO.find_all(session)
    return authors

@router_authors.get("/{id}", summary="Получить одного автора по id")
async def get_author_by_id(id: int) -> AuthorSchema:
    async with async_session_maker() as session:
        return await AuthorDAO.find_one_or_none_by_id(session=session,data_id=id)

@router_authors.put("/{id}", summary="Изменить одного автора по id")
async def update_author_info(id: int, author_data: AuthorAddSchema) -> AuthorSchema:
    async with async_session_maker() as session:
        return await AuthorDAO.update_one_by_id(session=session, data_id=id, values=author_data)

@router_authors.delete("/{id}", summary="Удалить одного автора по id")
async def delete_author(id: int):
    async with async_session_maker() as session:
        await AuthorDAO.delete_one_by_id(session=session, data_id=id)
        return {"message": "Author removed successfully"}

