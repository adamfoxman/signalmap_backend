from sqlalchemy.orm import Session

import app.models as models
import app.schemas as schemas

def get_countries(db: Session):
    return db.query(models.Country).all()


def get_country(db: Session,
                country: str):
    return db.query(models.Country).filter(models.Country.country_code == country).first()


# CREATE


def create_country(db: Session,
                   country: schemas.Country):
    db_country = models.Country(country_code=country.country_code,
                                is_enabled=False)
    db.add(db_country)
    db.commit()
    db.refresh(db_country)
    return db_country