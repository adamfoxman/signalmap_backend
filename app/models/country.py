from app.db.base_class import Base

from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import relationship


class Country(Base):
    __tablename__ = "countries"

    country_code = Column(String, index=True, primary_key=True)
    is_enabled = Column(Boolean, default=False)

    transmitters = relationship("Transmitter")