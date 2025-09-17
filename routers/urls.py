import asyncio

from fastapi import APIRouter, Depends, HTTPException, Path
from fastapi_cache.decorator import cache
from sqlalchemy.ext.asyncio import AsyncSession

from database.database import get_session
from repositories.url_repository import URLRepository
from schemas.short_url_schema import (InputUrlSchema, ShortUrlSchema,
                                      ShortUrlStat)
from utils.gen_short_code import gen_short_code

router = APIRouter(prefix="/shorten", tags=["Short Service"])


async def get_url_repo(session: AsyncSession = Depends(get_session)) -> URLRepository:
    return URLRepository(session)


@router.post("/", response_model=ShortUrlSchema, status_code=201)
async def shorten_the_link(
    url: InputUrlSchema,
    url_repo: URLRepository = Depends(get_url_repo),
    short_code: str = Depends(gen_short_code),
):
    new_url = await url_repo.create_short_url(url=url.url, short_code=short_code)

    return new_url


@router.get("/{short_code}", response_model=ShortUrlSchema, status_code=200)
@cache(expire=30)
async def get_url_by_short_code(
    short_code: str = Path(max_length=7),
    url_repo: URLRepository = Depends(get_url_repo),
):
    res = await url_repo.get_long_url_with_short(short_code)
    if not res:
        raise HTTPException(status_code=404, detail="URL not found")
    return res


@router.put("/{short_code}", response_model=ShortUrlSchema, status_code=200)
async def update_url_by_short_code(
    url: InputUrlSchema,
    short_code: str = Path(max_length=7),
    url_repo: URLRepository = Depends(get_url_repo),
):
    res = await url_repo.update_by_short_code(short_code, url.url)
    if res is None:
        raise HTTPException(status_code=404, detail="URL not found")
    return res


@router.delete("/{short_code}", status_code=204)
async def delete_url_by_short_code(
    short_code: str = Path(max_length=7),
    url_repo: URLRepository = Depends(get_url_repo),
):
    res = await url_repo.delete_by_short_code(short_code)
    if res == 0:
        raise HTTPException(status_code=404, detail="URL not found")


@router.get("/{short_code}/stats", response_model=ShortUrlStat, status_code=200)
async def get_count_by_short_code(
    short_code: str, url_repo: URLRepository = Depends(get_url_repo)
):
    res = await url_repo.get_long_url_with_short(short_code)
    if not res:
        raise HTTPException(status_code=404, detail="URL not found")
    return res
