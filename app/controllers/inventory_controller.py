from fastapi import HTTPException
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from sqlalchemy.orm import Session, joinedload
from ..utils.response_wrapper import APIResponse
from ..models.inventory_model import Inventory
from ..models.product_model import Product
from ..schemas.inventory_schema import InventoryCreate, InventoryUpdate, InventoryOut
from ..schemas.base_schema import PaginatedResponse
from decimal import Decimal

def create_inventory(db: Session, inventory: InventoryCreate):
    try:
        product = db.query(Product).filter(Product.id == inventory.product_id).first()
        if not product:
            raise HTTPException(
                status_code=404,
                detail="Product not found"
            )

        current_qty = Decimal(0)
        new_qty = current_qty + inventory.quantity_changed

        db_inventory = Inventory(
            product_id=inventory.product_id,
            quantity_changed=inventory.quantity_changed,
            quantity_before=current_qty,
            quantity_after=new_qty,
            threshold=inventory.threshold,
            reason=inventory.reason
        )

        db.add(db_inventory)
        db.commit()
        db.refresh(db_inventory)

        return APIResponse[InventoryOut](
            status=True,
            message="Inventory created successfully",
            data=db_inventory,
            error=None
        )

    except IntegrityError as e:
        db.rollback()
        raise HTTPException(
            status_code=400,
            detail=f"db error: {str(e)}"
        )
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail=f"db error: {str(e)}"
        )

def update_inventory_by_product(
    db: Session,
    product_id: str,
    inventory_update: InventoryUpdate
) -> APIResponse[InventoryOut]:
    try:
        product = db.query(Product).filter(Product.id == product_id).first()
        if not product:
            raise HTTPException(status_code=404, detail="Product not found")

        last_inventory = db.query(Inventory)\
            .filter(Inventory.product_id == product_id)\
            .order_by(Inventory.created_at.desc())\
            .first()

        current_qty = last_inventory.quantity_after if last_inventory else Decimal(0)
        new_qty = current_qty + inventory_update.quantity_changed
        threshold = inventory_update.threshold or (
            last_inventory.threshold if last_inventory else Decimal(10)
        )

        new_inventory = Inventory(
            product_id=product_id,
            quantity_before=current_qty,
            quantity_after=new_qty,
            quantity_changed=inventory_update.quantity_changed,
            threshold=threshold,
            reason=inventory_update.reason or "Stock adjustment",
        )

        db.add(new_inventory)
        db.commit()
        db.refresh(new_inventory)

        return APIResponse[InventoryOut](
            status=True,
            message="Inventory updated successfully",
            data=InventoryOut.model_validate(new_inventory),
            error=None
        )

    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")

def get_product_inventory_history(
    db: Session,
    product_id: str,
    page: int = 1,
    limit: int = 100
) -> APIResponse[PaginatedResponse[InventoryOut]]:
    try:
        page = max(1, page)
        limit = max(1, min(limit, 1000))
        offset = (page - 1) * limit

        query = db.query(Inventory)\
            .options(joinedload(Inventory.product))\
            .filter(Inventory.product_id == product_id)\
            .order_by(Inventory.created_at.desc())

        total_count = query.count()

        history = query.offset(offset).limit(limit).all()

        if not history:
            raise HTTPException(status_code=404, detail="No inventory records found")

        items = []
        for record in history:
            item_data = InventoryOut.model_validate({
                **record.__dict__,
                "product": {
                    "id": record.product.id,
                    "name": record.product.name,
                    "sku": record.product.sku,
                    "price": record.product.price,
                    "category_id": record.product.category_id,
                },
                "alert": record.quantity_after <= record.threshold
            })
            items.append(item_data)

        pagination = {
            "total_items": total_count,
            "total_pages": (total_count + limit - 1) // limit,
            "current_page": page,
            "page_size": limit,
            "items_on_page": len(items),
            "has_next": (page * limit) < total_count,
            "has_previous": page > 1
        }

        return APIResponse[PaginatedResponse[InventoryOut]](
            status=True,
            message="Inventory history retrieved successfully",
            data=PaginatedResponse[InventoryOut](
                items=items,
                pagination=pagination
            ),
            error=None
        )

    except SQLAlchemyError as e:
        raise HTTPException(
            status_code=500,
            detail=f"Database error: {str(e)}"
        )