from sqlalchemy import select, insert, delete, update, and_, desc
from app.database import async_session_maker
from app.articles.enums import Sorts


class BaseService:
    model = None

    @classmethod
    async def find_by_id(cls, id):
        async with async_session_maker() as session:
            query = select(cls.model).filter_by(id=id)
            result = await session.execute(query)
            return result.scalar_one_or_none()

    @classmethod
    async def find_one_or_none(cls, **filter_by):
        async with async_session_maker() as session:
            query = select(cls.model).filter_by(**filter_by)
            result = await session.execute(query)
            return result.scalar_one_or_none()

    @classmethod
    async def find_all(
        cls,
        limit: int,
        offset: int,
        sort: Sorts,
        **filters,
    ):
        conditions = []
        for field_name, value in filters.items():
            field = getattr(cls.model, field_name, None)

            if field is not None and value is not None:
                conditions.append(field == value)

        async with async_session_maker() as session:
            query = select(cls.model)

            if conditions:
                query = query.where(and_(*conditions))

            if sort:
                if sort == Sorts.NewOnesFirst:
                    query = query.order_by(desc(cls.model.created_at))
                else:
                    query = query.order_by(cls.model.created_at)

            query = query.limit(limit).offset(offset)
            result = await session.execute(query)
            return result.scalars().all()

    @classmethod
    async def add(cls, **data):
        async with async_session_maker() as session:
            query = insert(cls.model).values(**data).returning(cls.model)
            result = await session.execute(query)
            await session.commit()
            return result.scalar_one_or_none()

    @classmethod
    async def delete(cls, **data):
        async with async_session_maker() as session:
            query = delete(cls.model).filter_by(**data).returning(cls.model)
            result = await session.execute(query)
            await session.commit()
            return result.scalar_one_or_none()

    @classmethod
    async def update(cls, id: int, **data):
        async with async_session_maker() as session:
            query = (
                update(cls.model)
                .values(**data)
                .filter_by(
                    id=id,
                )
                .returning(cls.model)
            )
            result = await session.execute(query)
            await session.commit()
            return result.scalar_one_or_none()
