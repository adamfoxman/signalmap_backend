from app.db.base_class import Base

from enum import IntEnum as EnumType
from sqlalchemy import Column, ForeignKey, Float, String, CHAR, Integer, Enum, Boolean
from sqlalchemy.orm import relationship

from .intenum import IntEnum


# This represents possible transmitter types, as provided from FMList API
# MONO and STEREO is for FM radio transmissions
# DAB is for DAB and DAB+ digital radio
# DIGITAL_TV is for all digital TV transmissions
# the rest are for analog type TV transmissions
# class TransmitterType(EnumType):
#     NONE = 0
#     MONO = 1
#     STEREO = 2
#     DAB = 3
#     DIGITAL_TV = 4
#     ANALOGUE_TV = 5
#
#
# class RadiationPattern(EnumType):
#     NONE = 0
#     DIRECT = 1
#     NON_DIRECT = 2
#
#
# class Polarisation(EnumType):
#     NONE = 0
#     HORIZONTAL = 1
#     VERTICAL = 2
#     MIXED = 3
#     SLANT = 4
#     CIRCULAR = 5
#
#
# class Precision(EnumType):
#     NONE = 0
#     ONE_KM = 1
#     HUNDRED_METRES = 2
#     TEN_METRES = 3


class Transmitter(Base):
    __tablename__ = "transmitters"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    external_id = Column(Integer, index=True)  # id from external database
    frequency = Column(Float, index=True)
    mode = Column(String, index=True, default="")
    erp = Column(Float, default=1)
    antenna_height = Column(Integer, default=100)
    antenna_pattern = Column(String, default="ND")
    antenna_direction = Column(Integer)
    pattern_h = Column(String, default="")
    pattern_v = Column(String, default="")
    polarisation = Column(String, default="")
    location = Column(String)
    region = Column(String)
    country_id = Column(String, ForeignKey("countries.country_code"))
    latitude = Column(Float)
    longitude = Column(Float)
    precision = Column(Integer, default=0)
    height = Column(Integer, default=0)
    station = Column(String, default="")

    # country = relationship("Country", back_populates="transmitters")
