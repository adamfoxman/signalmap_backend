from typing import Any, List, Optional

from fastapi import APIRouter, Depends, HTTPException
# from sqlalchemy.orm import Session

from app import crud, models, schemas
from app.api import deps

router = APIRouter()


# GET
# -----------------------------------------------------------
@router.get("/code/", response_model=schemas.Country)
def get_country_by_country_code(country_code: str) -> Any:
    db = next(deps.get_db())
    country = crud.country.get_country(db, country_code)
    return country


@router.get("/", response_model=List[schemas.Country])
def get_countries() -> Any:
    db = next(deps.get_db())
    countries = crud.country.get_countries(db)
    return countries


# CREATE
# -----------------------------------------------------------
@router.post("/create/", response_model=schemas.Country)
def create_country(
        country_in: schemas.Country,
        current_user: models.User = Depends(deps.get_current_active_user)
) -> Any:
    if not crud.user.is_superuser(current_user):
        raise HTTPException(
            status_code=400,
            detail="The user doesn't have enough privileges"
        )
    else:
        db = next(deps.get_db())
        country = crud.country.create_country(db, country_in)
        return country


# UPDATE
# -----------------------------------------------------------
@router.put("/update/", response_model=schemas.Country)
def update_country(
        country_code: str,
        country_in: schemas.Country,
        current_user: models.User = Depends(deps.get_current_active_user)
):
    if not crud.user.is_superuser(current_user):
        raise HTTPException(
            status_code=400,
            detail="The user doesn't have enough privileges"
        )
    else:
        db = next(deps.get_db())
        country = crud.country.get_country(db, country_code)
        if not country:
            raise HTTPException(status_code=404, detail="Country not found")
        country = crud.country.update_country(db, country_code, country_in)
        return country


# DELETE
# -----------------------------------------------------------
@router.delete("/delete/", response_model=schemas.Country)
def delete_country(
        country_code: str,
        current_user: models.User = Depends(deps.get_current_active_user)
):
    if not crud.user.is_superuser(current_user):
        raise HTTPException(
            status_code=400,
            detail="The user doesn't have enough privileges"
        )
    else:
        db = next(deps.get_db())
        country = crud.country.get_country(db, country_code)
        if not country:
            raise HTTPException(status_code=404, detail="Country not found")
        country = crud.country.delete_country(db, country_code)
        return country
