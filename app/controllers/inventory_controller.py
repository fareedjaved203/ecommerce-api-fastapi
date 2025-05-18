from fastapi import HTTPException, status
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from sqlalchemy.orm import Session
from ..utils.response_wrapper import APIResponse
from ..models.inventory_model import Inventory
from ..models.product_model import Product
from ..schemas.inventory_schema import InventoryCreate, InventoryUpdate, InventoryOut
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
        # 1. Verify product exists
        product = db.query(Product).filter(Product.id == product_id).first()
        if not product:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Product not found"
            )

        # 2. Get the latest inventory record for this product
        inventory = db.query(Inventory)\
            .filter(Inventory.product_id == product_id)\
            .order_by(Inventory.created_at.desc())\
            .first()
            
        if not inventory:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="No inventory record found for this product"
            )

        # 3. Apply updates
        update_data = inventory_update.model_dump(exclude_unset=True)
        
        if 'quantity_changed' in update_data:
            # Calculate new quantity
            inventory.quantity_before = inventory.quantity_after
            inventory.quantity_after = inventory.quantity_after + update_data['quantity_changed']
        
        if 'threshold' in update_data:
            inventory.threshold = update_data['threshold']
            
        if 'reason' in update_data:
            inventory.reason = update_data['reason']

        db.commit()
        db.refresh(inventory)

        # 4. Check for low stock alert
        alert = inventory.quantity_after <= inventory.threshold

        return APIResponse[InventoryOut](
            status=True,
            message="Inventory updated successfully",
            data=inventory,
            error=None
        )

    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Database error: {str(e)}"
        )

def get_product_inventory(db: Session, product_id: str):
    try:
        product = db.query(Product).filter(Product.id == product_id).first()
        if not product:
            raise HTTPException(
                status_code=404,
                detail="Product not found"
            )

        inventory = db.query(Inventory)\
            .filter(Inventory.product_id == product_id)\
            .order_by(Inventory.created_at.desc())\
            .first()

        if not inventory:
            raise HTTPException(
                status_code=404,
                detail="No inventory records found for this product"
            )

        inventory_dict = InventoryOut.model_validate(inventory).model_dump()
        inventory_dict['alert'] = inventory.quantity_after <= inventory.threshold

        return APIResponse[Dict[str, Any]](
            status=True,
            message="Inventory retrieved successfully",
            data=inventory_dict,
            error=None
        )

    except SQLAlchemyError as e:
        raise HTTPException(
            status_code=500,
            detail=f"Database error: {str(e)}"
        )