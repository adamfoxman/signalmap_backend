import enum
from typing import List, Optional
from pydantic import BaseModel


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
    logo_token: Optional[int] = None
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
