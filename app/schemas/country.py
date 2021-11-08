from typing import List
from pydantic import BaseModel
from app.models.transmitter import Transmitter


class CountryBase(BaseModel):
    country_code: str
    is_enabled: bool


class CountryCreate(CountryBase):
    pass


class CountryUpdate(CountryBase):
    pass


class Country(CountryBase):
    class Config:
        orm_mode = True
