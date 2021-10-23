from sqlalchemy.orm import Session
from typing import List, Union, Any, Dict

from app.crud.crud_country import get_country
from app.models.transmitter import Transmitter as TransmitterModel, TransmitterType, Polarisation
from app.schemas.transmitter import TransmitterCreate, TransmitterInDB, TransmitterBase, TransmitterUpdate
# import app.schemas as schemas

from app.crud.base import CRUDBase


class CRUDTransmitter(CRUDBase[TransmitterModel, TransmitterCreate]):
    def get_transmitters_by_mode_country(self,
                                         db: Session,
                                         mode: str,
                                         country: str) -> List[TransmitterModel]:
        country_id = get_country(db, country)
        return db.query(TransmitterModel).filter(
            TransmitterModel.country_id == country_id
        ).filter(
            TransmitterModel.mode == TransmitterType[mode]
        )

    def get_transmitters(self,
                         db: Session,
                         mode: str,
                         country: str,
                         frequency: float = None,
                         erp: float = None,
                         polarisation: str = None,
                         location: str = None,
                         region: str = None,
                         station: str = None) -> List[TransmitterModel]:
        country_id = get_country(db, country)
        query = db.query(TransmitterModel).filter(
            TransmitterModel.country_id == country_id
        ).filter(TransmitterModel.mode == TransmitterType[mode])
        if frequency is not None:
            query = query.filter(TransmitterModel.frequency == frequency)
        if erp is not None:
            query = query.filter(TransmitterModel.erp == erp)
        if polarisation is not None:
            query = query.filter(TransmitterModel.polarisation ==
                                 Polarisation[polarisation])
        if location is not None:
            query = query.filter(TransmitterModel.location.find(location))
        if region is not None:
            query = query.filter(TransmitterModel.region.find(region))
        if station is not None:
            query = query.filter(TransmitterModel.station.find(station))

        return query

    def create_transmitter(self,
                           db: Session,
                           transmitter: TransmitterCreate) -> TransmitterModel:
        db_transmitter = TransmitterModel(external_id=transmitter.external_id,
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

    def update_transmitter(self, db: Session,
                           transmitter: TransmitterModel,
                           obj: Union[TransmitterUpdate, Dict[str, Any]]) -> TransmitterModel:
        if isinstance(obj, dict):
            update_data = obj
        else:
            update_data = obj.dict(exclude_unset=True)
        return super().update(db, db_obj=transmitter, obj_in=update_data)

    def delete_transmitter(self, db: Session,
                           transmitter: TransmitterModel,
                           id: int):
        db.query(transmitter).filter(TransmitterModel.id == id).delete()
        db.commit()

    def delete_transmitter_by_external_id(self, db: Session, transmitter: TransmitterModel, external_id: int):
        db.query(transmitter).filter(TransmitterModel.external_id == external_id).delete()
        db.commit()


transmitter = CRUDTransmitter(TransmitterModel)
