from typing import Any, List, Optional

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app import crud, models, schemas
from app.api import deps

router = APIRouter()


# GET
# ---------------------------------------------------------
@router.get("/get/id/", response_model=schemas.Transmitter)
def get_transmitter_by_id(
        id: int
) -> Any:
    db = next(deps.get_db())
    transmitter = crud.transmitter.get_transmitter_by_id(db, id)
    return transmitter


@router.get("/get/external/", response_model=schemas.Transmitter)
def get_transmitter_by_external_id(
        external_id: int,
) -> Any:
    db = next(deps.get_db())
    transmitter = crud.transmitter.get_transmitter_by_external_id(db, external_id)
    return transmitter


@router.get("/query/", response_model=List[schemas.Transmitter])
def get_transmitters(
        mode: str,
        country: str,
        frequency: Optional[float] = None,
        erp: Optional[float] = None,
        polarisation: Optional[str] = None,
        location: Optional[str] = None,
        region: Optional[str] = None,
        station: Optional[str] = None
):
    db = next(deps.get_db())
    transmitters = crud.transmitter.get_transmitters(
        db=db,
        mode=mode,
        country=country,
        frequency=frequency,
        erp=erp,
        polarisation=polarisation,
        location=location,
        region=region,
        station=station
    )
    return transmitters


# CREATE
# -----------------------------------------------------------
@router.post("/create/", response_model=schemas.Transmitter)
def create_transmitter(
        transmitter_in: schemas.Transmitter
) -> Any:
    db = next(deps.get_db())
    check_transmitter = crud.transmitter.get_transmitter_by_external_id(db, transmitter_in.external_id)
    if check_transmitter:
        raise HTTPException(status_code=400, detail="Transmitter already exists")
    else:
        transmitter = crud.transmitter.create_transmitter(db, transmitter=transmitter_in)
        return transmitter


# UPDATE
# -----------------------------------------------------------
@router.put("/update/", response_model=schemas.TransmitterInDB)
def update_transmitter(
        transmitter_id: int,
        transmitter_in: schemas.Transmitter
) -> Any:
    db = next(deps.get_db())
    transmitter = crud.transmitter.get_transmitter_by_id(db, transmitter_id)
    if not transmitter:
        raise HTTPException(status_code=404, detail="Transmitter not found")
    transmitter = crud.transmitter.update_transmitter(db, transmitter_id, transmitter_in)
    return transmitter


@router.put("/update/", response_model=schemas.TransmitterInDB)
def update_transmitter_by_external_id(
        external_id: int,
        transmitter_in: schemas.Transmitter
) -> Any:
    db = next(deps.get_db())
    transmitter = crud.transmitter.get_transmitter_by_external_id(db, external_id)
    if not transmitter:
        raise HTTPException(status_code=404, detail="Transmitter not found")
    transmitter = crud.transmitter.update_transmitter(db, external_id, transmitter_in)
    return transmitter


# DELETE
# -----------------------------------------------------------
@router.delete("/delete/", response_model=schemas.TransmitterInDB)
def delete_transmitter(
        transmitter_id: int
):
    db = next(deps.get_db())
    transmitter = crud.transmitter.get_transmitter_by_id(db, transmitter_id)
    if not transmitter:
        raise HTTPException(status_code=404, detail="Transmitter not found")
    transmitter = crud.transmitter.delete_transmitter(db, id=transmitter_id)
    return transmitter


@router.delete("/delete/external_id/", response_model=schemas.Transmitter)
def delete_transmitter_by_external_id(
        external_id: int
):
    db = next(deps.get_db())
    transmitter = crud.transmitter.get_transmitter_by_external_id(db, external_id)
    if not transmitter:
        raise HTTPException(status_code=404, detail="Transmitter not found")
    transmitter = crud.transmitter.delete_transmitter_by_external_id(db, external_id)
    return transmitter
