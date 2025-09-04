from datetime import datetime

from pydantic import BaseModel
from pydantic_settings import SettingsConfigDict


class InputUrlSchema(BaseModel):
    url: str


class ShortUrlSchema(BaseModel):
    id: int
    url: str
    shortCode: str
    createdAt: datetime
    updatedAt: datetime

    model_config = SettingsConfigDict(from_attributes=True)


class ShortUrlStat(ShortUrlSchema):
    accessCount: int
