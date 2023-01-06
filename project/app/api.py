from fastapi import FastAPI

from products.router import product_router

app = FastAPI(title="Product Project", debug=False)
app.include_router(product_router, prefix="/products")
