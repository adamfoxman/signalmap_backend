from sqlalchemy.orm import Session
from typing import List

from app.crud.crud_country import get_country
from app.models.transmitter import Transmitter, TransmitterType, Polarisation
from app.schemas.transmitter import TransmitterCreate
import app.schemas as schemas

from app.crud.base import CRUDBase


class CRUDTransmitter(CRUDBase[Transmitter, TransmitterCreate]):
    def get_transmitters_by_mode_country(self,
                                         db: Session,
                                         mode: str,
                                         country: str) -> List[Transmitter]:
        country_id = get_country(db, country)
        return db.query(Transmitter).filter(
            Transmitter.country_id == country_id
        ).filter(
            Transmitter.mode == TransmitterType[mode]
        )

    def get_transmitters(self,
                         db: Session,
                         mode: str,
                         country: str,
                         frequency: float = 0,
                         erp: float = 0,
                         polarisation: str = "not_provided",
                         location: str = "not_provided",
                         region: str = "not_provided",
                         station: str = "not_provided") -> List[Transmitter]:
        country_id = get_country(db, country)
        query = db.query(Transmitter).filter(
            Transmitter.country_id == country_id
        ).filter(Transmitter.mode == TransmitterType[mode])
        if frequency != 0:
            query = query.filter(Transmitter.frequency == frequency)
        if erp != 0:
            query = query.filter(Transmitter.erp == erp)
        if polarisation != "not_provided":
            query = query.filter(Transmitter.polarisation == Polarisation[polarisation])
        if location != "not_provided":
            query = query.filter(Transmitter.location.find(location))
        if region != "not_provided":
            query = query.filter(Transmitter.region.find(region))
        if station != "not_provided":
            query = query.filter(Transmitter.station.find(station))

        return query

    def create_transmitter(self,
                           db: Session,
                           transmitter: schemas.Transmitter) -> Transmitter:
        db_transmitter = Transmitter(external_id=transmitter.external_id,
                                     frequency=transmitter.frequency,
                                     mode=transmitter.mode,
                                     erp=transmitter.erp,
                                     antenna_height=transmitter.antenna_height,
                                     antenna_pattern=transmitter.antenna_pattern,
                                     antenna_direction=transmitter.antenna_direction,
                                     pattern_h=transmitter.pattern_h,
                                     pattern_v=transmitter.pattern_v,
                                     polarisation=transmitter.polarisation,
                                     location=transmitter.location,
                                     region=transmitter.region,
                                     country_id=transmitter.country_id,
                                     latitude=transmitter.latitude,
                                     longitude=transmitter.longitude,
                                     precision=transmitter.precision,
                                     height=transmitter.height,
                                     station=transmitter.station)
        db.add(db_transmitter)
        db.commit()
        db.refresh(db_transmitter)
        return db_transmitter


transmitter = CRUDTransmitter(Transmitter)