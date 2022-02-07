import enum
import math
from typing import List, Optional, Generic, TypeVar
from pydantic import BaseModel, Field, ValidationError
from pydantic.fields import ModelField


ExprType = TypeVar('ExprType')


# https://github.com/samuelcolvin/pydantic/issues/935
class Expr(Generic[ExprType]):
    validate_always = True

    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v, field: ModelField, values):
        result = eval(v, None, values)
        typ = field.sub_fields[0]
        validated, error = typ.validate(result, {}, loc='Expr')
        if error:
            raise ValidationError([error], cls)
        return validated


class TransmitterBase(BaseModel):
    external_id: int
    band: str
    frequency: float
    mode: Optional[str] = None
    erp: Optional[float] = None
    antenna_height: Optional[int] = None
    antenna_pattern: Optional[str] = None
    antenna_direction: Optional[str] = None
    pattern_h: Optional[str] = None
    pattern_v: Optional[str] = None
    polarisation: Optional[str] = None
    location: str
    region: Optional[str] = None
    country_id: str
    latitude: float
    longitude: float
    precision: Optional[int] = None
    height: Optional[int] = None
    station: Optional[str] = None
    station_id: Optional[int] = None
    logo_id: Optional[int] = None
    logo_token: Expr[int] = Field('int((float(station_id) * float(logo_id)) - (math.floor(float(station_id) / 345) * '
                                  'math.floor(float(logo_id) / 435)) + 45123)')
    coverage_file: Optional[str] = None
    north_bound: Optional[float] = None
    south_bound: Optional[float] = None
    east_bound: Optional[float] = None
    west_bound: Optional[float] = None


class TransmitterCreate(TransmitterBase):
    pass


class TransmitterUpdate(TransmitterBase):
    pass


class TransmitterInDB(TransmitterBase):
    id: int

    class Config:
        orm_mode = True


class Transmitter(TransmitterBase):
    class Config:
        orm_mode = True
