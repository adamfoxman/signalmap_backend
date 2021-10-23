from typing import List
from pydantic import BaseModel
from .transmitter import Transmitter


class CountryBase(BaseModel):
    country_code: str


class CountryCreate(CountryBase):
    pass


class Country(CountryBase):
    id: int
    transmitters: List[Transmitter] = []

    class Config:
        orm_mode = True
