from datetime import datetime
from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from clinicflow_api.database import get_session
from clinicflow_api.enums import AppointmentStatus
from clinicflow_api.exceptions import ConflictError, NotFoundError
from clinicflow_api.repositories import (
    AppointmentRepository,
    DoctorRepository,
    PatientRepository,
)
from clinicflow_api.schemas import (
    AppointmentCreate,
    AppointmentRead,
    AppointmentStatusUpdate,
    AppointmentUpdate,
)
from clinicflow_api.services import AppointmentService

router = APIRouter(prefix="/appointments", tags=["appointments"])


def get_service(
    session: Annotated[AsyncSession, Depends(get_session)],
) -> AppointmentService:
    return AppointmentService(
        AppointmentRepository(session),
        PatientRepository(session),
        DoctorRepository(session),
    )


Service = Annotated[AppointmentService, Depends(get_service)]


@router.post("", response_model=AppointmentRead, status_code=status.HTTP_201_CREATED)
async def create_appointment(data: AppointmentCreate, service: Service):
    try:
        return await service.create(data)
    except NotFoundError as exc:
        raise HTTPException(status.HTTP_404_NOT_FOUND, str(exc)) from exc
    except ConflictError as exc:
        raise HTTPException(status.HTTP_409_CONFLICT, str(exc)) from exc


@router.get("", response_model=list[AppointmentRead])
async def list_appointments(
    service: Service,
    skip: Annotated[int, Query(ge=0)] = 0,
    limit: Annotated[int, Query(ge=1, le=100)] = 50,
    patient_id: UUID | None = None,
    doctor_id: UUID | None = None,
    status_: Annotated[AppointmentStatus | None, Query(alias="status")] = None,
    date_from: datetime | None = None,
    date_to: datetime | None = None,
):
    return await service.list(
        skip=skip,
        limit=limit,
        patient_id=patient_id,
        doctor_id=doctor_id,
        status=status_,
        date_from=date_from,
        date_to=date_to,
    )


@router.get("/{appointment_id}", response_model=AppointmentRead)
async def get_appointment(appointment_id: UUID, service: Service):
    try:
        return await service.get(appointment_id)
    except NotFoundError as exc:
        raise HTTPException(status.HTTP_404_NOT_FOUND, str(exc)) from exc


@router.patch("/{appointment_id}", response_model=AppointmentRead)
async def update_appointment(
    appointment_id: UUID, data: AppointmentUpdate, service: Service
):
    try:
        return await service.update(appointment_id, data)
    except NotFoundError as exc:
        raise HTTPException(status.HTTP_404_NOT_FOUND, str(exc)) from exc
    except ConflictError as exc:
        raise HTTPException(status.HTTP_409_CONFLICT, str(exc)) from exc


@router.patch("/{appointment_id}/status", response_model=AppointmentRead)
async def change_appointment_status(
    appointment_id: UUID, data: AppointmentStatusUpdate, service: Service
):
    try:
        return await service.change_status(appointment_id, data)
    except NotFoundError as exc:
        raise HTTPException(status.HTTP_404_NOT_FOUND, str(exc)) from exc
    except ConflictError as exc:
        raise HTTPException(status.HTTP_409_CONFLICT, str(exc)) from exc
