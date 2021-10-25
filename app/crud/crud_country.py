from sqlalchemy.orm import Session

from app.models.country import Country as CountryModel
from app.schemas.country import Country, CountryBase, CountryCreate
import app.schemas as schemas

from app.crud.base import CRUDBase


class CRUDCountry(CRUDBase[Country, CountryBase, CountryCreate]):
    def get_countries(self, 
                      db: Session) -> list[Country]:
        return db.query(CountryModel).all()

    def get_country(self, db: Session,
                    country: str) -> CountryModel:
        return db.query(CountryModel).filter(CountryModel.country_code == country).first()

    def create_country(self, db: Session,
                       country: CountryBase) -> CountryModel:
        db_country = CountryModel(country_code=country.country_code,
                                  is_enabled=False)
        db.add(db_country)
        db.commit()
        db.refresh(db_country)
        return db_country

    def delete_country(self, db: Session, country: CountryBase, country_code: str):
        db.query(country).filter(country.country_code == country_code).delete()
        db.commit()


def get_country(db: Session,
                country: str) -> CountryModel:
    return db.query(CountryModel).filter(CountryModel.country_code == country).first()


country = CRUDCountry(CountryModel)
