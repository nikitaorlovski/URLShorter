from sqlalchemy import delete, select, update
from sqlalchemy.ext.asyncio.session import AsyncSession

from models.url_model import URLModel


class URLRepository:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def create_short_url(self, url: str, short_code: str) -> URLModel:
        new_shorted_url = URLModel(url=url, shortCode=short_code)
        self.session.add(new_shorted_url)
        await self.session.flush()
        await self.session.commit()
        return new_shorted_url

    async def get_long_url_with_short(self, short_code: str) -> URLModel:
        res = await self.session.execute(
            select(URLModel).where(URLModel.shortCode == short_code)
        )
        url = res.scalar_one_or_none()
        return url

    async def update_by_short_code(self, short_code: str, url: str) -> URLModel | None:
        res = await self.session.execute(
            select(URLModel).where(URLModel.shortCode == short_code)
        )
        model_res = res.scalar_one_or_none()
        if model_res is None:
            return None
        model_res.url = url
        await self.session.commit()
        await self.session.refresh(model_res)
        return model_res

    async def delete_by_short_code(self, short_code: str):
        res = await self.session.execute(
            delete(URLModel).where(URLModel.shortCode == short_code)
        )
        await self.session.commit()
        return res.rowcount

    async def increment_and_get_url(self, short_code: str) -> URLModel | None:
        stmt = await self.session.execute(
            update(URLModel)
            .where(URLModel.shortCode == short_code)
            .values(accessCount=URLModel.accessCount + 1)
        )
        await self.session.commit()
        if stmt.rowcount == 0:
            return None
        res = await self.session.execute(
            select(URLModel).where(URLModel.shortCode == short_code)
        )
        return res.scalar_one_or_none()
