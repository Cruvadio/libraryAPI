from typing import Generic, TypeVar, List, Dict, Any
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from .database import Base
from .models import Author, Book, Borrow
from sqlalchemy import select
from pydantic import BaseModel

T = TypeVar("T", bound=Base)
class BaseDAO(Generic[T]):
    model: type[T]  # Устанавливается в дочернем классе

    @classmethod
    async def add(cls, session: AsyncSession, **values):
        # Добавить одну запись
        new_instance = cls.model(**values)
        session.add(new_instance)
        try:
            await session.commit()
        except SQLAlchemyError as e:
            await session.rollback()
            raise e
        return new_instance

    @classmethod
    async def add_many(cls, session: AsyncSession, instances: List[Dict[str, Any]]):
        new_instances = [cls.model(**values) for values in instances]
        session.add_all(new_instances)
        try:
            await session.commit()
        except SQLAlchemyError as e:
            await session.rollback()
            raise e
        return new_instances

    @classmethod
    async def find_one_or_none_by_id(cls, data_id: int, session: AsyncSession):
        query = select(cls.model).filter_by(id=data_id)
        result = await session.execute(query)
        record = result.scalar_one_or_none()
        return record

    @classmethod
    async def find_all(cls, session: AsyncSession, filters: BaseModel | None = None):
        if filters:
            filter_dict = filters.model_dump(exclude_unset=True)
        else:
            filter_dict = {}
        try:
            query = select(cls.model).filter_by(**filter_dict)
            result = await session.execute(query)
            records = result.scalars().all()
            return records
        except SQLAlchemyError as e:
            raise

    @classmethod
    async def update_one_by_id(cls, session: AsyncSession, data_id: int, values: BaseModel):
        values_dict = values.model_dump()
        try:
            record = await session.get(cls.model, data_id)
            for key, value in values_dict.items():
                if value:
                    setattr(record, key, value)
            await session.commit()
            return record
        except SQLAlchemyError as e:
            print(e)
            raise e

    @classmethod
    async def delete_one_by_id(cls, data_id: int, session: AsyncSession):
        # Найти запись по ID
        try:
            data = await session.get(cls.model, data_id)
            if data:
                await session.delete(data)
                await session.commit()
        except SQLAlchemyError as e:
            print(f"Error occurred: {e}")
            raise

class AuthorDAO(BaseDAO[Author]):
    model = Author


class BookDAO(BaseDAO[Book]):
    model = Book

class BorrowDAO(BaseDAO[Borrow]):
    model = Borrow