from sqlalchemy.orm import Session
from app.models import Base, Product, Inventory, Sale, SaleItem, Platform
from ..db.database import engine, SessionLocal
import logging
from datetime import datetime, timedelta
import random
from decimal import Decimal

logger = logging.getLogger(__name__)

def seed_sales_data():
    db = SessionLocal()
    try:
        if db.query(Sale).count() > 0:
            return False 
        
        products = db.query(Product).all()
        platforms = db.query(Platform).all()
        
        for i in range(50): 
            sale_date = datetime.utcnow() - timedelta(days=random.randint(0, 365))
            
            sale = Sale(
                total_amount=0, 
                platform_id=random.choice(platforms).id,
                sale_date=sale_date,
                created_at=sale_date,
                updated_at=sale_date
            )
            db.add(sale)
            db.flush() 
            
            total_amount = Decimal('0')
            for _ in range(random.randint(1, 5)):
                product = random.choice(products)
                quantity = random.randint(1, 10)
                price = product.price
                item_total = price * quantity
                
                db.add(SaleItem(
                    product_id=product.id,
                    sales_id=sale.id,
                    quantity=quantity,
                    per_item_price=price,
                    total_price=item_total
                ))
                total_amount += item_total
            
            sale.total_amount = total_amount
            db.commit()
        
        return True
    except Exception as e:
        db.rollback()
        raise

def seed_initial_data():
    db = SessionLocal()
    try:
        if db.query(Product).count() > 0:
            logger.info("Data already seeded - skipping")
            return False

        logger.info("Seeding initial data...")
        
        products = [
            Product(name="Premium Headphones", sku="PH-100", price=199.99),
            Product(name="Wireless Mouse", sku="WM-200", price=29.99),
            Product(name="Mechanical Keyboard", sku="MK-300", price=129.99)
        ]
        db.add_all(products)
        db.commit()

        inventories = [
            Inventory(
                product_id=products[0].id,
                quantity_before=0,
                quantity_after=100,
                threshold=10,
                reason="Initial stock"
            ),
            Inventory(
                product_id=products[1].id,
                quantity_before=0,
                quantity_after=200,
                threshold=20,
                reason="Initial stock"
            )
        ]
        db.add_all(inventories)
        db.commit()

        logger.info("Data seeding completed successfully")
        return True

    except Exception as e:
        db.rollback()
        logger.error(f"Data seeding failed: {str(e)}")
        raise
    finally:
        db.close()