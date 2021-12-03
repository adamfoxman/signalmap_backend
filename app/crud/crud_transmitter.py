from sqlalchemy.orm import Session
from typing import List, Union, Any, Dict, Optional

from app.api.deps import get_db
from app.crud.crud_country import get_country
from app.models.transmitter import Transmitter as TransmitterModel
from app.schemas.transmitter import TransmitterCreate, TransmitterInDB, TransmitterBase, TransmitterUpdate

from app.crud.base import CRUDBase


class CRUDTransmitter(CRUDBase[TransmitterModel, TransmitterCreate, TransmitterUpdate]):
    def get_transmitters_by_mode_country(self,
                                         db: Session,
                                         band: str,
                                         country: str) -> List[TransmitterModel]:
        country_id = get_country(db, country)
        return db.query(TransmitterModel).filter(
            TransmitterModel.country_id == country_id
        ).filter(
            TransmitterModel.band == band
        )

    def get_transmitters(self,
                         db: Session,
                         band: str,
                         country: str,
                         frequency: Optional[float] = None,
                         erp: Optional[float] = None,
                         polarisation: Optional[str] = None,
                         location: Optional[str] = None,
                         region: Optional[str] = None,
                         station: Optional[str] = None) -> List[TransmitterModel]:
        country_id = get_country(db, country)
        query = db.query(TransmitterModel).filter(
            TransmitterModel.country_id == country_id
        ).filter(TransmitterModel.band == band)
        if frequency is not None:
            query = query.filter(TransmitterModel.frequency == frequency)
        if erp is not None:
            query = query.filter(TransmitterModel.erp == erp)
        if polarisation is not None:
            query = query.filter(TransmitterModel.polarisation == polarisation)
        if location is not None:
            query = query.filter(TransmitterModel.location.find(location))
        if region is not None:
            query = query.filter(TransmitterModel.region.find(region))
        if station is not None:
            query = query.filter(TransmitterModel.station.find(station))

        return query

    def get_transmitter_by_id(self,
                              db: Session,
                              transmitter_id: int) -> TransmitterModel:
        query = db.query(TransmitterModel).filter(TransmitterModel.id == transmitter_id).first()
        return query

    def get_transmitter_by_external_id(self, db: Session, band: str, external_id: int) -> TransmitterModel:
        query = db.query(TransmitterModel).filter(
            TransmitterModel.band == band
        ).filter(
            TransmitterModel.external_id == external_id
        ).first()
        return query

    def create_transmitter(self,
                           db: Session,
                           transmitter: TransmitterCreate) -> TransmitterModel:
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
                                          kml_file=transmitter.kml_file,
                                          coverage_file=transmitter.coverage_file)
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
