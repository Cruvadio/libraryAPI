import datetime

from app.schemas import BorrowSchema, BorrowAddSchema
from app.database import async_session_maker
from app.dao import BorrowDAO
from fastapi import APIRouter, Response, status

router_borrows = APIRouter(prefix='/borrows', tags=['Информация о выдачах книг'])
@router_borrows.post("/",
                     summary="Создание записи о выдачи. Невозможно при отсутсвие экземпляров книг",
                     status_code=status.HTTP_201_CREATED)
async def add_borrow(borrow_data: BorrowAddSchema):
    async with async_session_maker() as session:
        return await BorrowDAO.add_borrow(session=session, **borrow_data.dict())


@router_borrows.get("/", summary="Получить информацию о всех выдачах", response_model=list[BorrowSchema])
async def get_borrows()-> list[BorrowSchema]:
    async with async_session_maker() as session:
        authors = await BorrowDAO.find_all(session)
    return authors

@router_borrows.get("/{id}", summary="Получить информацию о выдаче по id")
async def get_borrow_by_id(id: int) -> BorrowSchema:
    async with async_session_maker() as session:
        return await BorrowDAO.find_one_or_none_by_id(session=session, data_id=id)
@router_borrows.patch("/{id}/return", summary="Вернуть книгу")
async def finish_borrow(id: int, date_of_return: datetime.date):
    async with async_session_maker() as session:
        await BorrowDAO.finish_borrow(session, id, date_of_return)