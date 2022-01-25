from app.db.base_class import Base

from sqlalchemy import Column, ForeignKey, Float, String, CHAR, Integer, Enum, Boolean
from sqlalchemy.orm import relationship


class Transmitter(Base):
    __tablename__ = "transmitters"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    external_id = Column(Integer, index=True)  # id from external database
    band = Column(String, index=True)
    frequency = Column(Float, index=True)
    mode = Column(String, index=True, default="")
    erp = Column(Float, default=1)
    antenna_height = Column(Integer, default=100)
    antenna_pattern = Column(String, default="ND")
    antenna_direction = Column(String, default="")
    pattern_h = Column(String, default="")
    pattern_v = Column(String, default="")
    polarisation = Column(String, default="")
    location = Column(String)
    region = Column(String, default="")
    country_id = Column(String, ForeignKey("countries.country_code"))
    latitude = Column(Float)
    longitude = Column(Float)
    precision = Column(Integer, default=0)
    height = Column(Integer, default=0)
    station = Column(String, default="")
    station_id = Column(Integer, default=0)
    logo_id = Column(Integer, default=0)
    logo_token = Column(Integer, default=0)
    coverage_file = Column(String, default="")
    north_bound = Column(Float, default=0)
    south_bound = Column(Float, default=0)
    east_bound = Column(Float, default=0)
    west_bound = Column(Float, default=0)

    country = relationship("Country", back_populates="transmitters")
