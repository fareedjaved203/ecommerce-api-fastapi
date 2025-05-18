from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import Annotated
from ..db.database import get_db
from ..schemas.category_schema import CategoryCreate, CategoryUpdate, CategoryOut
from ..controllers.category_controller import (
    list_categories,
    retrieve_category,
    create_category,
    update_category,
    delete_category,
)

router = APIRouter(prefix="/categories", tags=["Categories"])

db_dependency = Annotated[Session, Depends(get_db)]

@router.get("/", response_model=list[CategoryOut])
def get_all_categories(db: db_dependency):
    return list_categories(db)


@router.get("/{category_id}", response_model=CategoryOut)
def get_category(category_id: str, db: db_dependency):
    return retrieve_category(category_id, db)


@router.post("/", response_model=CategoryOut)
def create_new_category(payload: CategoryCreate, db: db_dependency):
    return create_category(payload, db)


@router.put("/{category_id}", response_model=CategoryOut)
def update_existing_category(category_id: str, payload: CategoryUpdate, db: db_dependency):
    return update_category(category_id, payload, db)


@router.delete("/{category_id}")
def remove_category(category_id: str, db: db_dependency):
    return delete_category(category_id, db)