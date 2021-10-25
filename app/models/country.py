from app.db.base_class import Base

from sqlalchemy import Column, Integer, String, Boolean
from sqlalchemy.orm import relationship


class Country(Base):
    __tablename__ = "countries"

    id = Column(Integer, primary_key=True, index=True)
    country_code = Column(String, index=True)
    is_enabled = Column(Boolean, default=False)

    transmitters = relationship("Transmitter", back_populates="country")