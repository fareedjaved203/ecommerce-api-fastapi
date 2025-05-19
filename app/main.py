from fastapi import FastAPI
from .routers.category_router import router as category_router
from .routers.product_router import router as product_router
from .routers.platform_router import router as platform_router
from .routers.inventory_router import router as inventory_router
from .routers.order_router import router as order_router
from .routers.sales_analysis_router import router as sales_router

from .db.database import engine
from app import models

app = FastAPI()
models.Base.metadata.create_all(bind=engine)

app.include_router(category_router, prefix="/api/v1")
app.include_router(product_router, prefix="/api/v1")
app.include_router(platform_router, prefix="/api/v1")
app.include_router(inventory_router, prefix="/api/v1")
app.include_router(order_router, prefix="/api/v1")
app.include_router(sales_router, prefix="/api/v1")

@app.get("/")
def root():
    return {"message": "E commerce backend is running!"}