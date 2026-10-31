from typing import Annotated
from uuid import UUID

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession

from clinicflow_api.database import get_session
from clinicflow_api.exceptions import ConflictError, NotFoundError
from clinicflow_api.repositories import SpecialtyRepository
from clinicflow_api.schemas import SpecialtyCreate, SpecialtyRead, SpecialtyUpdate
from clinicflow_api.services import SpecialtyService

router = APIRouter(prefix="/specialties", tags=["specialties"])


def get_service(
    session: Annotated[AsyncSession, Depends(get_session)],
) -> SpecialtyService:
    return SpecialtyService(SpecialtyRepository(session))


Service = Annotated[SpecialtyService, Depends(get_service)]


@router.post("", response_model=SpecialtyRead, status_code=status.HTTP_201_CREATED)
async def create_specialty(data: SpecialtyCreate, service: Service):
    try:
        return await service.create(data)
    except ConflictError as exc:
        raise HTTPException(status.HTTP_409_CONFLICT, str(exc)) from exc


@router.get("", response_model=list[SpecialtyRead])
async def list_specialties(
    service: Service,
    skip: Annotated[int, Query(ge=0)] = 0,
    limit: Annotated[int, Query(ge=1, le=100)] = 50,
):
    return await service.list(skip, limit)


@router.get("/{specialty_id}", response_model=SpecialtyRead)
async def get_specialty(specialty_id: UUID, service: Service):
    try:
        return await service.get(specialty_id)
    except NotFoundError as exc:
        raise HTTPException(status.HTTP_404_NOT_FOUND, str(exc)) from exc


@router.patch("/{specialty_id}", response_model=SpecialtyRead)
async def update_specialty(specialty_id: UUID, data: SpecialtyUpdate, service: Service):
    try:
        return await service.update(specialty_id, data)
    except NotFoundError as exc:
        raise HTTPException(status.HTTP_404_NOT_FOUND, str(exc)) from exc
    except ConflictError as exc:
        raise HTTPException(status.HTTP_409_CONFLICT, str(exc)) from exc


@router.delete("/{specialty_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_specialty(specialty_id: UUID, service: Service):
    try:
        await service.delete(specialty_id)
    except NotFoundError as exc:
        raise HTTPException(status.HTTP_404_NOT_FOUND, str(exc)) from exc
    except ConflictError as exc:
        raise HTTPException(status.HTTP_409_CONFLICT, str(exc)) from exc
