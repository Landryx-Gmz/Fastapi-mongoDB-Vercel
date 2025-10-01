from fastapi import FastAPI

from routers import products
from routers import user


app = FastAPI()

# Routers
app.include_router(products.router)
app.include_router(user.router)

@app.get("/")
async def root():
    return "!Hola FastAPI"

@app.get("/url")
async def url():
    return {"url_curso": "https://mouredev.com/python"}