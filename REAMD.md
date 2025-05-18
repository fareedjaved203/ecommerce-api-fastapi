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

- View current inventory status
- Receive alerts for low stock items
- Update stock levels
- Track inventory changes over time

### Sales and Revenue Analytics

- Retrieve sales data by product, category, or platform
- Filter sales by day, week, month, year, or a custom range
- Compare revenue across time periods and categories
- Identify top and bottom-performing products

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
uvicorn app.main:app --reload
```
## API ENDPOINTS

### PRODUCT

GET /categories/ – Retrieve all categories

POST /products/ – Add a new product

GET /inventory/status – Check current inventory and low stock alerts

GET /sales/compare – Compare sales across products, dates, or categories

GET /revenue/summary – Get revenue breakdown by time period


## API Documentation:

http://localhost:8000/docs

## References

FastAPI Documentation: https://fastapi.tiangolo.com/

SQLAlchemy 2.0: https://docs.sqlalchemy.org/en/20/

Pydantic v2: https://docs.pydantic.dev/

MVC Architecture: https://verticalserve.medium.com/building-a-python-fastapi-crud-api-with-mvc-structure-13ec7636d8f2


### by Fareed Javed