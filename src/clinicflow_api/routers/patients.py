from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from clinicflow_api.database import get_session
from clinicflow_api.repositories import PatientRepository
from clinicflow_api.schemas import PatientCreate, PatientRead, PatientUpdate
from clinicflow_api.services import ConflictError, NotFoundError, PatientService

router = APIRouter(prefix="/patients", tags=["patients"])


def get_service(
    session: Annotated[AsyncSession, Depends(get_session)],
) -> PatientService:
    return PatientService(PatientRepository(session))


Service = Annotated[PatientService, Depends(get_service)]


@router.post("", response_model=PatientRead, status_code=status.HTTP_201_CREATED)
async def create_patient(data: PatientCreate, service: Service):
    try:
        return await service.create(data)
    except ConflictError as exc:
        raise HTTPException(status.HTTP_409_CONFLICT, str(exc)) from exc


@router.get("", response_model=list[PatientRead])
async def list_patients(
    service: Service,
    skip: Annotated[int, Query(ge=0)] = 0,
    limit: Annotated[int, Query(ge=1, le=100)] = 50,
    q: Annotated[str | None, Query(max_length=100)] = None,
):
    return await service.list(skip=skip, limit=limit, q=q)


@router.get("/{patient_id}", response_model=PatientRead)
async def get_patient(patient_id: UUID, service: Service):
    try:
        return await service.get(patient_id)
    except NotFoundError as exc:
        raise HTTPException(status.HTTP_404_NOT_FOUND, str(exc)) from exc


@router.patch("/{patient_id}", response_model=PatientRead)
async def update_patient(patient_id: UUID, data: PatientUpdate, service: Service):
    try:
        return await service.update(patient_id, data)
    except NotFoundError as exc:
        raise HTTPException(status.HTTP_404_NOT_FOUND, str(exc)) from exc
    except ConflictError as exc:
        raise HTTPException(status.HTTP_409_CONFLICT, str(exc)) from exc


@router.delete("/{patient_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_patient(patient_id: UUID, service: Service):
    try:
        await service.delete(patient_id)
    except NotFoundError as exc:
        raise HTTPException(status.HTTP_404_NOT_FOUND, str(exc)) from exc
