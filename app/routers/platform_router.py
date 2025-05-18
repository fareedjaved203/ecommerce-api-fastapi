from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Annotated

from ..utils.response_wrapper import APIResponse
from ..db.database import get_db
from ..schemas.platform_schema import PlatformCreate, PlatformUpdate, PlatformOut
from ..schemas.base_schema import PaginatedResponse
from ..controllers.platform_controller import (
    get_platform,
    get_platforms,
    create_platform,
    update_platform,
    delete_platform
)

db_dependency = Annotated[Session, Depends(get_db)]

router = APIRouter(prefix="/platforms", tags=["platforms"])

@router.post("/", response_model=APIResponse[PlatformOut])
def create_new_platform(platform: PlatformCreate, db: db_dependency):
    return create_platform(db, platform)

@router.get("/", response_model=APIResponse[PaginatedResponse[PlatformOut]])
def read_platforms(
    db: db_dependency,
    page: int = 1,
    limit: int = 100,
    search: str = "",
):
    return get_platforms(db, page=page, limit=limit, search=search)

@router.get("/{platform_id}", response_model=APIResponse[PlatformOut])
def read_platform(platform_id: int, db: db_dependency):
    db_platform = get_platform(db, platform_id)
    if db_platform is None:
        raise HTTPException(status_code=404, detail="Platform not found")
    return db_platform

@router.put("/{platform_id}", response_model=APIResponse[PlatformOut])
def update_existing_platform(platform_id: int, platform: PlatformUpdate, db: db_dependency):
    db_platform = update_platform(db, platform_id, platform)
    if db_platform is None:
        raise HTTPException(status_code=404, detail="Platform not found")
    return db_platform

@router.delete("/{platform_id}")
def delete_existing_platform(platform_id: int, db: db_dependency):
    success = delete_platform(db, platform_id)
    if not success:
        raise HTTPException(status_code=404, detail="Platform not found")
    return {"message": "Platform deleted successfully"}