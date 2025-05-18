from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import Annotated, List

from ..db.database import get_db
from ..utils.response_wrapper import APIResponse
from ..schemas.category_schema import CategoryCreate, CategoryUpdate, CategoryOut
from ..schemas.base_schema import PaginatedResponse
from ..controllers.category_controller import (
    list_categories,
    retrieve_category,
    create_category,
    update_category,
    delete_category,
)

router = APIRouter(prefix="/categories", tags=["Categories"])

db_dependency = Annotated[Session, Depends(get_db)]

@router.get("/", response_model=APIResponse[PaginatedResponse[CategoryOut]])
def get_categories(
    page: int = 1,
    limit: int = 100,
    search: str = "",
    db: Session = Depends(get_db)
):
    return list_categories(db, page=page, limit=limit, search=search)


@router.get("/{category_id}", response_model=APIResponse[CategoryOut])
def get_category(category_id: str, db: db_dependency):
    return retrieve_category(category_id, db)


@router.post("/", response_model=APIResponse[CategoryOut])
def create_new_category(payload: CategoryCreate, db: db_dependency):
    return create_category(payload, db)


@router.put("/{category_id}", response_model=APIResponse[CategoryOut])
def update_existing_category(category_id: str, payload: CategoryUpdate, db: db_dependency):
    return update_category(category_id, payload, db)


@router.delete("/{category_id}")
def remove_category(category_id: str, db: db_dependency):
    return delete_category(category_id, db)