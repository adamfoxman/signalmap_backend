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
                    country_code: str) -> CountryModel:
        return db.query(CountryModel).filter(CountryModel.country_code == country_code).first()

    def create_country(self, db: Session,
                       country: CountryBase) -> CountryModel:
        db_country = CountryModel(country_code=country.country_code,
                                  country_name=country.country_name,
                                  is_enabled=country.is_enabled)
        db.add(db_country)
        db.commit()
        db.refresh(db_country)
        return db_country

    def update_country(self, db: Session, country_code: str,
                       obj: Union[Country, Dict[Country, Any]]) -> CountryModel:
        if isinstance(obj, dict):
            update_data = obj
        else:
            update_data = obj.dict(exclude_unset=True)
        db.query(CountryModel).filter(CountryModel.country_code == country_code).update(update_data)
        db.commit()
        return db.query(CountryModel).filter(CountryModel.country_code == country_code).first()

    def delete_country(self, db: Session, country_code: str) -> CountryModel:
        model = db.query(CountryModel).filter(CountryModel.country_code == country_code).first()
        db.delete(model)
        db.commit()
        return model


def get_country(db: Session,
                country: str) -> CountryModel:
    return db.query(CountryModel).filter(CountryModel.country_code == country).first()


country = CRUDCountry(CountryModel)
