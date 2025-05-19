from decimal import Decimal
from datetime import datetime, timezone
from fastapi import HTTPException, status
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session
from typing import Optional
from ..models.sale_model import Sale
from ..models.sale_item_model import SaleItem
from ..models.product_model import Product
from ..models.inventory_model import Inventory
from ..schemas.sale_item_schema import SaleOut, SaleIn, SaleItemOut
from ..utils.response_wrapper import APIResponse

def create_order(
    db: Session,
    order_data: SaleIn
) -> SaleOut:
    try:
        effective_date = order_data.sale_date if order_data.sale_date is not None else datetime.now(timezone.utc)
        product_ids = [item.product_id for item in order_data.items]
        
        products = db.query(Product)\
            .filter(Product.id.in_(product_ids))\
            .all()
        
        if len(products) != len(product_ids):
            missing = set(product_ids) - {p.id for p in products}
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Products not found: {missing}"
            )

        product_map = {p.id: p for p in products}
        inventory_updates = {}
        
        for item in order_data.items:
            product = product_map[item.product_id]
            inventory = db.query(Inventory)\
                .filter(Inventory.product_id == product.id)\
                .order_by(Inventory.created_at.desc())\
                .first()
            
            if inventory is None or inventory.quantity_after < item.quantity:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=f"Product {product.id} doesn't have enough stock"
                )
            
            inventory_updates[product.id] = {
                'current': inventory,
                'quantity': item.quantity
            }

        total_amount = Decimal('0')
        sale = Sale(
            platform_id=order_data.platform_id,
            total_amount=Decimal('0'),
            sale_date=effective_date
        )
        db.add(sale)
        db.flush()

        sale_items = []
        for item in order_data.items:
            product = product_map[item.product_id]
            inventory_data = inventory_updates[product.id]
            price = Decimal(str(product.price))
            item_total = price * Decimal(str(item.quantity))
            
            sale_item = SaleItem(
                product_id=product.id,
                sales_id=sale.id,
                quantity=item.quantity,
                per_item_price=price,
                total_price=item_total
            )
            db.add(sale_item)
            sale_items.append(sale_item)
            
            db.add(Inventory(
                product_id=product.id,
                quantity_before=inventory_data['current'].quantity_after,
                quantity_after=inventory_data['current'].quantity_after - item.quantity,
                threshold=inventory_data['current'].threshold,
                quantity_changed=-item.quantity,
                reason=f"Sold in order {sale.id}"
            ))
            
            total_amount += item_total

        sale.total_amount = total_amount
        db.commit()
        
        data = SaleOut(
            id=sale.id,
            platform_id=sale.platform_id,
            total_amount=sale.total_amount,
            sale_date=sale.sale_date,
            items=[
                SaleItemOut(
                    product_id=item.product_id,
                    quantity=item.quantity,
                    per_item_price=item.per_item_price,
                    total_price=item.total_price
                ) for item in sale_items
            ]
        )
        
        return APIResponse[SaleOut](
            status=True,
            message="Order created successfully",
            data=data,
            error=None
        )

    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Database error: {str(e)}"
        )
    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(e)
        )