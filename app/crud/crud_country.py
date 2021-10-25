from typing import Union, List, Dict, Any

from sqlalchemy.orm import Session

from app.models.country import Country as CountryModel
from app.schemas.country import Country, CountryBase, CountryCreate, CountryUpdate

from app.crud.base import CRUDBase


class CRUDCountry(CRUDBase[Country, CountryBase, CountryCreate]):
    def get_countries(self, 
                      db: Session) -> List[Country]:
        return db.query(CountryModel).all()

    def get_country(self, db: Session,
                    country: str) -> CountryModel:
        return db.query(CountryModel).filter(CountryModel.country_code == country).first()

    def get_country_by_id(self, db: Session, country_id: int) -> CountryModel:
        return db.query(CountryModel).filter(CountryModel.id == country_id).first()

    def create_country(self, db: Session,
                       country: CountryBase) -> CountryModel:
        db_country = CountryModel(country_code=country.country_code,
                                  is_enabled=False)
        db.add(db_country)
        db.commit()
        db.refresh(db_country)
        return db_country

    def update_country(self, db: Session, country: CountryModel,
                       obj: Union[CountryUpdate, Dict[str, Any]]) -> CountryModel:
        if isinstance(obj, dict):
            update_data = obj
        else:
            update_data = obj.dict(exclude_unset=True)
        return super().update(db, db_obj=country, obj_in=update_data)

    def delete_country(self, db: Session, country_id: int, country: CountryModel = CountryModel):
        country_tbd = db.query(country).filter(country.id == country_id).first()
        country_tbd.delete()
        db.commit()
        return country_tbd

    def delete_country_by_code(self, db: Session, country_code: str, country: CountryModel = CountryModel):
        country_tbd = db.query(country).filter(country.country_code == country_code).first()
        country_tbd.delete()
        db.commit()
        return country_tbd


def get_country(db: Session,
                country: str) -> CountryModel:
    return db.query(CountryModel).filter(CountryModel.country_code == country).first()


country = CRUDCountry(CountryModel)
