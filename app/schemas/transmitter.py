import enum
from typing import List, Optional
from pydantic import BaseModel


class TransmitterBase(BaseModel):
    external_id: int
    band: str
    frequency: float
    mode: str
    erp: float
    antenna_height: int
    antenna_pattern: str
    antenna_direction: str
    pattern_h: Optional[str] = None
    pattern_v: Optional[str] = None
    polarisation: str
    location: str
    region: str
    country_id: str
    latitude: float
    longitude: float
    precision: int
    height: int
    station: str
    kml_file: Optional[str] = None
    coverage_file: Optional[str] = None


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
