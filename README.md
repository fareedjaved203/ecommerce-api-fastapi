# Admin Dashboard API – FastAPI

This is a monolithic, MVC-structured Admin Dashboard API built using FastAPI and SQLAlchemy 2.0. It helps managers effectively manage products, categories, inventory, and sales performance across multiple e-commerce platforms like Amazon, Walmart, and Alibaba.

## Overview

The Admin Dashboard API enables admin users to:

- Add, edit, hide/unhide, and manage products and categories
- Track sales across multiple online platforms
- Analyze sales and revenue data by day, week, month, year, or a custom date range
- Compare revenue by category, product, or date range
- Monitor and manage inventory levels, including stock changes and low stock alerts
- Identify best-selling and least-selling products over time

## ERD Diagram with Explanation

![alt text](image.png)

## Tech Stack

- Python 3.12
- FastAPI 0.115.0
- Uvicorn 0.34.0
- SQLAlchemy 2.0.x
- PyMySQL 1.1.0
- Pydantic 2.11.x
- Typing 3.7+

## Product and Category Rules

- Maximum product quantity: 99,999
- Maximum product price: $9,999.99

## Features

### Category, Platform and Product Management

- Create, update, list, and delete categories, platform and products
- Platform help the managers to keep a track of the platform on which the product sold i.e. Amazon, Wallmart, Flipcart, Alibaba etc.
- Hide or unhide products from being listed
- Pagination and search for category, platform and product

### Inventory Management

- View current inventory status such as quantity changed like +100/-100, quantity before and quantity after. Threshold level after which it will show the alert levels and the reason for a certain inventory change
- Receive alerts for low stock items in the form of boolean
- Update stock levels by changing the quantity such as +100 (adding) or -100 (removing)
- Track inventory changes over time by showing complete history in the inventory

### Order Placement

- place orders based on platform, products and its quantities
- changes reflects the inventory levels

### Sales and Revenue Analytics

- Retrieve sales data by product, category, or platform
- Filter sales by day, week, month, year, or a custom range
- Compare revenue across time periods and categories

## Getting Started

### Installation

1. Clone the repository:

```bash
git clone https://github.com/yourusername/admin-dashboard-api.git
```
2. Navigate to the path
```bash
cd admin-dashboard-api
```

3. Setup virtual environment
```
python -m venv venv
venv\Scripts\activate
```

4. Install the dependencies
```bash
pip install -r requirements.txt
```

5. Create .env file in your root folder and add the following database url, don't forget to add your username, password and database name
```
DB_URL=mysql+pymysql://user:password@localhost:3306/yourdb
```

6. Create database in your MySQL database by adding the following command
```
CREATE DATABASE ecommercedashboard;
```

7. Run migrations using alembic
```
alembic upgrade head
```

8. Start the development server
```
uvicorn app.main:app --port 5000
```

## Seed

- All the necessary data populates when the server starts

## API Endpoints

Base URL: `/`

---

### Categories

- **GET** `/api/v1/categories/`  
  Retrieve all categories.

- **POST** `/api/v1/categories/`  
  Create a new category.

- **GET** `/api/v1/categories/{category_id}`  
  Retrieve a category by its ID.

- **PUT** `/api/v1/categories/{category_id}`  
  Update an existing category by ID.

- **DELETE** `/api/v1/categories/{category_id}`  
  Delete a category by ID.

---

### Products

- **GET** `/api/v1/products/`  
  List all products.

- **POST** `/api/v1/products/`  
  Create a new product.

- **GET** `/api/v1/products/{product_id}`  
  Retrieve a product by ID.

- **PUT** `/api/v1/products/{product_id}`  
  Update an existing product by ID.

- **DELETE** `/api/v1/products/{product_id}`  
  Delete a product by ID.

---

### Platforms

- **GET** `/api/v1/platforms/`  
  List all platforms.

- **GET** `/api/v1/platforms/{platform_id}`  
  Retrieve a platform by ID.

- **PUT** `/api/v1/platforms/{platform_id}`  
  Update an existing platform by ID.

- **DELETE** `/api/v1/platforms/{platform_id}`  
  Delete a platform by ID.

---

### Inventory

- **PUT** `/api/v1/inventory/product/{product_id}`  
  Create or update inventory for a specific product.

- **GET** `/api/v1/inventory/product/{product_id}`  
  Retrieve complete inventory history, with each interaction, for a product with low stock alerts(boolean).

---

### Orders

- **POST** `/api/v1/orders/`  
  Place a new order.
  Stock changes are reflected in the inventory as well.

---

### Revenue

- **GET** `/api/v1/revenue/daily`  
  Get daily revenue summary.

- **GET** `/api/v1/revenue/weekly`  
  Get weekly revenue summary.

- **GET** `/api/v1/revenue/monthly`  
  Get monthly revenue summary.

- **GET** `/api/v1/revenue/annual`  
  Get annual revenue summary.

- **GET** `/api/v1/revenue/custom`  
  Get revenue data for a custom date range.

- **POST** `/api/v1/revenue/compare`  
  Compare revenue for different dates (more than 2).

- **POST** `/api/v1/revenue/compare-by-category`  
  Compare revenue across categories (more than 2).

---

## API Documentation:

http://localhost:8000/docs

## References

FastAPI Documentation: https://fastapi.tiangolo.com/

SQLAlchemy 2.0: https://docs.sqlalchemy.org/en/20/

Pydantic v2: https://docs.pydantic.dev/

MVC Architecture: https://verticalserve.medium.com/building-a-python-fastapi-crud-api-with-mvc-structure-13ec7636d8f2


### by Fareed Javed
