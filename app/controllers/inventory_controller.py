from fastapi import HTTPException
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from sqlalchemy.orm import Session, joinedload
from ..utils.response_wrapper import APIResponse
from ..models.inventory_model import Inventory
from ..models.product_model import Product
from ..schemas.inventory_schema import InventoryCreate, InventoryUpdate, InventoryOut
from ..schemas.product_schema import ProductOut
from decimal import Decimal
from typing import Dict, Any

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

        inventory = db.query(Inventory)\
            .filter(Inventory.product_id == product_id)\
            .order_by(Inventory.created_at.desc())\
            .first()
            
        if not inventory:
            raise HTTPException(status_code=404, detail="No inventory record found")

        current_alert_status = inventory.quantity_after <= inventory.threshold

        update_data = inventory_update.model_dump(exclude_unset=True)
        
        if 'quantity_changed' in update_data:
            inventory.quantity_before = inventory.quantity_after
            inventory.quantity_after += update_data['quantity_changed']
            inventory.quantity_changed = update_data['quantity_changed']
        
        if 'threshold' in update_data:
            inventory.threshold = update_data['threshold']
            
        if 'reason' in update_data:
            inventory.reason = update_data['reason']

        new_alert_status = inventory.quantity_after <= inventory.threshold
        
        if bool(current_alert_status) != bool(new_alert_status):
            inventory.alert = new_alert_status

        db.commit()
        db.refresh(inventory)

        response_data = InventoryOut.model_validate(inventory)
        response_data.alert = bool(new_alert_status)

        return APIResponse[InventoryOut](
            status=True,
            message="Inventory updated successfully",
            data=response_data,
            error=None
        )

    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail=f"Database error: {str(e)}"
        )

def get_product_inventory(db: Session, product_id: str):
    try:
        inventory = db.query(Inventory)\
            .options(joinedload(Inventory.product))\
            .filter(Inventory.product_id == product_id)\
            .order_by(Inventory.created_at.desc())\
            .first()

        if not inventory:
            raise HTTPException(status_code=404, detail="No inventory records found")

        response_data = InventoryOut.model_validate({
            **inventory.__dict__,
            "product": inventory.product,
            "alert": inventory.quantity_after <= inventory.threshold
        })

        return APIResponse[InventoryOut](
            status=True,
            message="Inventory retrieved successfully",
            data=response_data,
            error=None
        )

    except SQLAlchemyError as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")