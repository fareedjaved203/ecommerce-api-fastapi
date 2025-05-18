from fastapi import FastAPI
from .routers.category_router import router as category_router
from .routers.product_router import router as product_router

app = FastAPI()

app.include_router(category_router, prefix="/api/v1")
app.include_router(product_router, prefix="/api/v1")

@app.get("/")
def root():
    return {"message": "E commerce backend is running!"}