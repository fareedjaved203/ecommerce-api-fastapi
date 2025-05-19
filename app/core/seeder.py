from sqlalchemy.orm import Session
from app.models import Product, Inventory, Category, Platform
from ..controllers.order_controller import create_order
from ..schemas.sale_item_schema import SaleIn, SaleItemIn
from decimal import Decimal
from ..db.database import SessionLocal 
from sqlalchemy.exc import IntegrityError
import random
from sqlalchemy import select
from datetime import datetime, timedelta, timezone
from sqlalchemy import func

def seed_categories():
    db: Session = SessionLocal()
    categories = [
        {"name": "Electronics", "sku": "electronics-001"},
        {"name": "Fashion", "sku": "fashion-002"},
        {"name": "Home & Kitchen", "sku": "home-kitchen-003"},
        {"name": "Health & Personal Care", "sku": "health-care-004"},
        {"name": "Sports & Outdoors", "sku": "sports-outdoors-005"},
        {"name": "Books", "sku": "books-006"},
        {"name": "Toys & Games", "sku": "toys-games-007"},
        {"name": "Automotive", "sku": "automotive-008"},
        {"name": "Beauty", "sku": "beauty-009"},
        {"name": "Office Supplies", "sku": "office-supplies-010"}
    ]


    for cat in categories:
        existing = db.query(Category).filter_by(name=cat["name"]).first()
        if not existing:
            try:
                new_category = Category(**cat)
                db.add(new_category)
                db.commit()
            except IntegrityError:
                db.rollback()
                print(f"Category {cat['name']} already exists. Skipping.")
            except Exception as e:
                db.rollback()
                print(f"Error adding {cat['name']}: {e}")
    db.close()

def seed_products():
    db: Session = SessionLocal()

    categories = db.query(Category).all()
    if not categories:
        print("No categories found. Skipping product seeding.")
        return

    product_names = [
        f"Product {i}" for i in range(1, 51)
    ]

    for i, name in enumerate(product_names):
        sku = f"{name.lower().replace(' ', '-')}-{random.randint(1000,9999)}"
        price = Decimal(f"{random.randint(100, 10000) / 100:.2f}")
        description = f"Description for {name}"
        category = random.choice(categories)

        existing_product = db.query(Product).filter_by(sku=sku).first()
        if existing_product:
            continue

        try:
            product = Product(
                name=name,
                sku=sku,
                price=price,
                published=bool(random.getrandbits(1)),
                description=description,
                category_id=category.id
            )
            db.add(product)
            db.commit()
        except IntegrityError:
            db.rollback()
        except Exception as e:
            db.rollback()
            print(f"Error adding product {name}: {e}")

    db.close()
    
    
def seed_inventory_history():
    db: Session = SessionLocal()
    products = db.query(Product).all()

    if not products:
        print("No products found. Skipping inventory seeding.")
        return

    for product in products:
        last_inventory = (
            db.query(Inventory)
            .filter(Inventory.product_id == product.id)
            .order_by(Inventory.created_at.desc())
            .first()
        )

        quantity_before = last_inventory.quantity_after if last_inventory else Decimal(0)
        quantity_changed = Decimal(random.randint(5, 50))
        quantity_after = quantity_before + quantity_changed
        threshold = Decimal(random.choice([50, 75, 100]))
        reason = f"Initial stock added for {product.name}"

        try:
            inventory = Inventory(
                product_id=product.id,
                quantity_before=quantity_before,
                quantity_after=quantity_after,
                quantity_changed=quantity_changed,
                threshold=threshold,
                reason=reason,
                created_at=datetime.utcnow()
            )
            db.add(inventory)
            db.commit()
        except IntegrityError:
            db.rollback()
        except Exception as e:
            db.rollback()
            print(f"Error adding inventory for {product.name}: {e}")

    db.close()
    
    
def seed_platforms():
    db: Session = SessionLocal()
    platforms = [
        "Amazon", "Walmart", "Alibaba", "eBay", "Etsy",
        "Flipkart", "AliExpress", "Target", "Rakuten", "BigCommerce"
    ]

    for name in platforms:
        existing = db.query(Platform).filter(func.lower(Platform.name) == func.lower(name)).first()
        if existing:
            print(f"Platform {name} already exists. Skipping.")
            continue
        try:
            platform = Platform(name=name)
            db.add(platform)
            db.commit()
        except IntegrityError:
            db.rollback()
        except Exception as e:
            db.rollback()
            print(f"Error creating platform {name}: {e}")

    db.close()
    
def seed_orders():
    db: Session = SessionLocal()

    products = db.execute(select(Product)).scalars().all()
    if not products:
        print("No products found in DB. Skipping order seeding.")
        return

    platforms = db.execute(select(Platform)).scalars().all()
    if not platforms:
        print("No platforms found in DB. Skipping order seeding.")
        return

    for _ in range(50):
        product = random.choice(products)
        platform = random.choice(platforms)

        inventory = db.execute(
            select(Product)
            .filter(Product.id == product.id)
            .join(Product.inventories)
            .order_by(Product.inventories.property.mapper.class_.created_at.desc())
        ).scalars().first()

        if not product.inventories:
            print(f"Skipping product {product.id} due to missing inventory")
            continue

        latest_inventory = product.inventories[-1]
        max_qty = int(latest_inventory.quantity_after)

        if max_qty <= 0:
            print(f"Skipping product {product.id} due to insufficient stock")
            continue

        quantity = random.randint(1, min(5, max_qty))

        days_ago = random.randint(1, 365)
        sale_date = datetime.now(timezone.utc) - timedelta(days=days_ago)

        order_data = SaleIn(
            platform_id=platform.id,
            sale_date=sale_date,
            items=[
                SaleItemIn(
                    product_id=product.id,
                    quantity=quantity
                )
            ]
        )

        try:
            create_order(db, order_data)
        except Exception as e:
            print(f"Failed to create order: {e}")
    
    db.close()