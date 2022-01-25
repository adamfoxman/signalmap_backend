import math

from sqlalchemy.orm import Session
from typing import List, Union, Any, Dict, Optional

from app.api.deps import get_db
from app.crud.crud_country import get_country
from app.models.transmitter import Transmitter as TransmitterModel
from app.schemas.transmitter import TransmitterCreate, TransmitterInDB, TransmitterBase, TransmitterUpdate, Transmitter

from app.crud.base import CRUDBase


def calculate_image_token(station_id: int, logo_id: int) -> int:
    if station_id <= 0 or logo_id <= 0:
        return 0
    return int((float(station_id) * float(logo_id)) -
               (math.floor(float(station_id) / 345) * math.floor(float(logo_id) / 435)) + 45123)


class CRUDTransmitter(CRUDBase[TransmitterInDB, TransmitterCreate, TransmitterUpdate]):
    def get_transmitters_by_band_country(self,
                                         db: Session,
                                         band: str,
                                         country: str) -> List[TransmitterInDB]:
        country_id = get_country(db, country)
        return db.query(TransmitterModel).filter(
            TransmitterModel.country_id == country
        ).filter(
            TransmitterModel.band == band
        ).all()

    def get_transmitters(self,
                         db: Session,
                         band: str,
                         country: str,
                         frequency: Optional[float] = None,
                         erp: Optional[float] = None,
                         polarisation: Optional[str] = None,
                         location: Optional[str] = None,
                         region: Optional[str] = None,
                         station: Optional[str] = None) -> List[TransmitterInDB]:
        query = db.query(TransmitterModel).filter(
            TransmitterModel.country_id == country
        ).filter(TransmitterModel.band == band)
        if frequency is not None:
            query = query.filter(TransmitterModel.frequency == frequency)
        if erp is not None:
            query = query.filter(TransmitterModel.erp == erp)
        if polarisation is not None:
            query = query.filter(TransmitterModel.polarisation == polarisation)
        if location is not None:
            loc = f'%{location}%'
            query = query.filter(TransmitterModel.location.ilike(loc))
        if region is not None:
            reg = f'%{region}%'
            query = query.filter(TransmitterModel.region.ilike(reg))
        if station is not None:
            sta = f'%{station}%'
            query = query.filter(TransmitterModel.station.ilike(sta))
        return query.all()

    def get_transmitter_by_id(self,
                              db: Session,
                              transmitter_id: int) -> TransmitterInDB:
        query = db.query(TransmitterModel).filter(TransmitterModel.id == transmitter_id).first()
        return query

    def get_transmitter_by_external_id(self, db: Session, band: str, external_id: int) -> TransmitterInDB:
        query = db.query(TransmitterModel).filter(
            TransmitterModel.band == band
        ).filter(
            TransmitterModel.external_id == external_id
        ).first()
        return query

    def create_transmitter(self,
                           db: Session,
                           transmitter: TransmitterCreate) -> TransmitterModel:
        t = self.get_transmitter_by_external_id(db, transmitter.band, transmitter.external_id)
        if t is None:
            logo_token = calculate_image_token(transmitter.station_id, transmitter.logo_id)
            db_transmitter = TransmitterModel(external_id=transmitter.external_id,
                                              band=transmitter.band,
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
                                              station=transmitter.station,
                                              station_id=transmitter.station_id,
                                              logo_id=transmitter.logo_id,
                                              logo_token=logo_token,
                                              coverage_file=transmitter.coverage_file,
                                              north_bound=transmitter.north_bound,
                                              south_bound=transmitter.south_bound,
                                              east_bound=transmitter.east_bound,
                                              west_bound=transmitter.west_bound)
            db.add(db_transmitter)
            db.commit()
            db.refresh(db_transmitter)
            return db_transmitter

    def update_transmitter(self, db: Session,
                           transmitter: TransmitterModel,
                           obj: Union[TransmitterUpdate, Dict[TransmitterModel, Any]]) -> TransmitterModel:
        if isinstance(obj, dict):
            update_data = obj
        else:
            update_data = obj.dict(exclude_unset=True)
        db.query(TransmitterModel).filter(TransmitterModel.id == transmitter.id).update(update_data)
        db.commit()
        return db.query(TransmitterModel).filter(TransmitterModel.id == transmitter.id).first()

    def delete_transmitter(self, db: Session,
                           id: int) -> TransmitterModel:
        model = db.query(TransmitterModel).filter(TransmitterModel.id == id).first()
        db.delete(model)
        db.commit()
        return model

    def delete_transmitter_by_external_id(self, db: Session, band: str, external_id: int):
        model = db.query(TransmitterModel).filter(
            TransmitterModel.band == band
        ).filter(
            TransmitterModel.external_id == external_id
        ).first()
        db.delete(model)
        db.commit()
        return model


transmitter = CRUDTransmitter(TransmitterModel)
