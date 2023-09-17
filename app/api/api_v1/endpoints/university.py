from typing import List
from uuid import UUID

from fastapi import APIRouter, Depends, Security

from app.api import deps
from app.common.exceptions import RecordNotFoundException, RecordNotFoundHTTPException
from app.university.schemas.university import UniversityCreate, UniversityUpdate, UniversityView
from app.university.services.university_service import UniversityService

router = APIRouter()
validate_token = deps.token_auth()


@router.post("/", response_model=UniversityView, dependencies=[Security(validate_token)])
def create_university(
    university: UniversityCreate,
    service: UniversityService = Depends(deps.get_university_service),
):
    return service.create(create=university)


@router.get("/", response_model=List[UniversityView], dependencies=[Security(validate_token)])
def get_all(
    service: UniversityService = Depends(deps.get_university_service),
):
    return service.get_all()


@router.get(
    "/{id_university}", response_model=UniversityView, dependencies=[Security(validate_token)]
)
def get_by_id(
    id_university: UUID, service: UniversityService = Depends(deps.get_university_service)
):
    try:
        return service.get_by_id(id_university=id_university)
    except RecordNotFoundException:
        raise RecordNotFoundHTTPException(detail="University not found")


@router.put(
    "/{id_university}", response_model=UniversityView, dependencies=[Security(validate_token)]
)
def update_university(
    id_university: UUID,
    update: UniversityUpdate,
    service: UniversityService = Depends(deps.get_university_service),
):
    try:
        return service.update(id_university=id_university, update=update)
    except RecordNotFoundException:
        raise RecordNotFoundHTTPException(detail="University not found")


@router.delete("/{id_university}", dependencies=[Security(validate_token)])
def delete_university(
    id_university: UUID,
    service: UniversityService = Depends(deps.get_university_service),
):
    try:
        service.delete(id_university=id_university)
    except RecordNotFoundException:
        raise RecordNotFoundHTTPException(detail="University not found")
