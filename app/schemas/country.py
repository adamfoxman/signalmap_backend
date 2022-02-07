from pydantic import BaseModel


class CountryBase(BaseModel):
    country_code: str
    country_name: str
    is_enabled: bool


class CountryCreate(CountryBase):
    pass


class CountryUpdate(CountryBase):
    pass


class Country(CountryBase):
    class Config:
        orm_mode = True
