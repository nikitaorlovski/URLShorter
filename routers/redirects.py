from fastapi import APIRouter, Depends, Path
from fastapi.exceptions import HTTPException
from fastapi.responses import RedirectResponse

from repositories.url_repository import URLRepository
from routers.urls import get_url_repo

router = APIRouter(tags=["Redirect URL"])


@router.get("/{short_code}", status_code=302)
async def redirect(
    short_code: str = Path(max_length=7),
    url_repo: URLRepository = Depends(get_url_repo),
):
    res = await url_repo.increment_and_get_url(short_code)
    if not res:
        raise HTTPException(status_code=404, detail="URL not found")
    return RedirectResponse(url=res.url, status_code=302)
