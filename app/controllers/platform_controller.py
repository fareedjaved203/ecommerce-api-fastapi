from fastapi import HTTPException
from sqlalchemy.orm import Session
from typing import List
from sqlalchemy import func

from ..models.platform_model import Platform
from ..utils.response_wrapper import APIResponse
from ..schemas.platform_schema import PlatformCreate, PlatformUpdate, PlatformOut
from ..schemas.base_schema import PaginatedResponse


def get_platform(db: Session, platform_id: int):
    platform =  db.query(Platform).filter(Platform.id == platform_id).first()
    return APIResponse[PlatformOut](
        status=True,
        message="Platform retrieved successfully",
        data=platform,
        error=None
    )

def get_platforms(
    db: Session,
    page: int = 1,
    limit: int = 100,
    search: str = ""
) -> APIResponse[PaginatedResponse[PlatformOut]]:
    try:
        if page < 1:
            page = 1
        if limit < 1:
            limit = 100
            
        skip = (page - 1) * limit
        
        query = db.query(Platform)
        
        if search:
            query = query.filter(Platform.name.ilike(f"%{search}%"))
        
        platforms = query.offset(skip).limit(limit).all()
        
        total_count = query.with_entities(func.count(Platform.id)).scalar()
        
        page_count = (total_count + limit - 1) // limit if limit > 0 else 1
        current_page = page
        
        response_data = {
            "items": platforms,
            "pagination": {
                "total_items": total_count,
                "total_pages": page_count,
                "current_page": current_page,
                "page_size": limit,
                "items_on_page": len(platforms),
                "has_next": (page * limit) < total_count,
                "has_previous": page > 1
            }
        }
        
        return APIResponse[PaginatedResponse[PlatformOut]](
            status=True,
            message="Platforms retrieved successfully",
            data=response_data,
            error=None
        )
        
    except Exception as e:
        print(f"Error: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Error: {str(e)}"
        )
        
def create_platform(db: Session, platform: PlatformCreate):
    existing_platform = db.query(Platform).filter(func.lower(Platform.name) == func.lower(platform.name)).first()
        
    if existing_platform:
        raise HTTPException(
            status_code=409,
            detail="Platform with this name exists"
    )
        
    db_platform = Platform(**platform.model_dump())
    db.add(db_platform)
    db.commit()
    db.refresh(db_platform)
    
    return APIResponse[PlatformOut](
        status=True,
        message="Platform created successfully",
        data=db_platform,
        error=None
    )

def update_platform(db: Session, platform_id: int, platform: PlatformUpdate):
    db_platform = get_platform(db, platform_id)
    if not db_platform:
        raise HTTPException(
            status_code=404,
            detail="Platform not found"
        )
    
    if platform.name is not None:
        existing_platform = db.query(Platform).filter(
            func.lower(Platform.name) == func.lower(platform.name),
            Platform.id != platform_id
        ).first()
        
        if existing_platform:
            raise HTTPException(
                status_code=409,
                detail="Another platform with this name already exists"
            )
            
        db_platform.name = platform.name
    
    db.commit()
    db.refresh(db_platform)
    
    return APIResponse[PlatformOut](
        status=True,
        message="Platform updated successfully",
        data=db_platform,
        error=None
    )

def delete_platform(db: Session, platform_id: int):
    db_platform = get_platform(db, platform_id)
    if not db_platform:
        return False
    
    db.delete(db_platform)
    db.commit()
    return APIResponse[None](
        status=True,
        message="Platform deleted successfully",
        data=None,
        error=None
    )