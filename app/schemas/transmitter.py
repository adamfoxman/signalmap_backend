import enum
from typing import List, Optional
from pydantic import BaseModel


class TransmitterBase(BaseModel):
    external_id: int
    frequency: float
    mode: enum.Enum
    erp: float
    antenna_height: int
    antenna_pattern: enum.Enum
    antenna_direction: Optional[int] = None
    pattern_h: Optional[str] = None
    pattern_v: Optional[str] = None
    polarisation: enum.Enum
    location: str
    region: str
    country_id: int
    latitude: float
    longitude: float
    precision: enum.Enum
    height: int
    station: str


class TransmitterCreate(TransmitterBase):
    pass


class Transmitter(TransmitterBase):
    id: int

    class Config:
        orm_mode = True