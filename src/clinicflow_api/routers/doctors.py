from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from clinicflow_api.database import get_session
from clinicflow_api.repositories import (
    AppointmentRepository,
    DoctorRepository,
    SpecialtyRepository,
)
from clinicflow_api.schemas import DoctorCreate, DoctorRead, DoctorUpdate
from clinicflow_api.services import ConflictError, DoctorService, NotFoundError

router = APIRouter(prefix="/doctors", tags=["doctors"])


def get_service(
    session: Annotated[AsyncSession, Depends(get_session)],
) -> DoctorService:
    return DoctorService(
        DoctorRepository(session),
        SpecialtyRepository(session),
        AppointmentRepository(session),
    )


Service = Annotated[DoctorService, Depends(get_service)]


@router.post("", response_model=DoctorRead, status_code=status.HTTP_201_CREATED)
async def create_doctor(data: DoctorCreate, service: Service):
    try:
        return await service.create(data)
    except NotFoundError as exc:
        raise HTTPException(status.HTTP_404_NOT_FOUND, str(exc)) from exc
    except ConflictError as exc:
        raise HTTPException(status.HTTP_409_CONFLICT, str(exc)) from exc


@router.get("", response_model=list[DoctorRead])
async def list_doctors(
    service: Service,
    skip: Annotated[int, Query(ge=0)] = 0,
    limit: Annotated[int, Query(ge=1, le=100)] = 50,
    specialty_id: UUID | None = None,
    is_active: bool | None = None,
):
    return await service.list(
        skip=skip, limit=limit, specialty_id=specialty_id, is_active=is_active
    )


@router.get("/{doctor_id}", response_model=DoctorRead)
async def get_doctor(doctor_id: UUID, service: Service):
    try:
        return await service.get(doctor_id)
    except NotFoundError as exc:
        raise HTTPException(status.HTTP_404_NOT_FOUND, str(exc)) from exc


@router.patch("/{doctor_id}", response_model=DoctorRead)
async def update_doctor(doctor_id: UUID, data: DoctorUpdate, service: Service):
    try:
        return await service.update(doctor_id, data)
    except NotFoundError as exc:
        raise HTTPException(status.HTTP_404_NOT_FOUND, str(exc)) from exc
    except ConflictError as exc:
        raise HTTPException(status.HTTP_409_CONFLICT, str(exc)) from exc


@router.delete("/{doctor_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_doctor(doctor_id: UUID, service: Service):
    try:
        await service.delete(doctor_id)
    except NotFoundError as exc:
        raise HTTPException(status.HTTP_404_NOT_FOUND, str(exc)) from exc
    except ConflictError as exc:  # nuevo
        raise HTTPException(status.HTTP_409_CONFLICT, str(exc)) from exc
