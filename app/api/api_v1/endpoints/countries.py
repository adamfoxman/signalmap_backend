from typing import Any, List, Optional

from fastapi import APIRouter, Depends, HTTPException
# from sqlalchemy.orm import Session

from app import crud, models, schemas
from app.api import deps

router = APIRouter()


# GET
# -----------------------------------------------------------
@router.get("/id/", response_model=schemas.Country)
def get_country(
        id: int
) -> Any:
    db = deps.get_db()
    country = crud.country.get_country_by_id(db, id)
    return country


@router.get("/code", response_model=schemas.Country)
def get_country_by_country_code(country_code: str) -> Any:
    db = deps.get_db()
    country = crud.country.get_country(db, country_code)
    return country


@router.get("/", response_model=List[schemas.Country])
def get_countries() -> Any:
    db = deps.get_db()
    countries = crud.country.get_countries(db)
    return countries


# CREATE
# -----------------------------------------------------------
@router.post("/create/", response_model=schemas.Country)
def create_country(
        country_in: schemas.Country
) -> Any:
    db = deps.get_db()
    new_country = crud.country.create_country(db,
                                              country=country_in)
    return new_country


# UPDATE
# -----------------------------------------------------------
@router.put("/update/", response_model=schemas.Country)
def update_country(
        country_id: int,
        country_in: schemas.Country
):
    db = deps.get_db()
    country = crud.country.get_country_by_id(db, country_id)
    if not country:
        raise HTTPException(status_code=404, detail="Country not found")
    country = crud.country.update_country(db, country_id, country_in)
    return country


# DELETE
# -----------------------------------------------------------
@router.delete("/delete/", response_model=schemas.Country)
def delete_country(
        country_id: int
):
    db = deps.get_db()
    country = crud.country.get_country_by_id(db, country_id)
    if not country:
        raise HTTPException(status_code=404, detail="Country not found")
    country = crud.country.delete_country(db, country_id)
    return country


@router.delete("/delete/country_code/", response_model=schemas.Country)
def delete_country_by_code(
        country_code: str
):
    db = deps.get_db()
    country = crud.country.get_country_by_code(db, country_code)
    if not country:
        raise HTTPException(status_code=404, detail="Country not found")
    country = crud.country.delete_country_by_code(db, country_code)
    return country
