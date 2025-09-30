from fastapi import FastAPI

from routers import products


app = FastAPI()

# Routers
app.include_router(products.router)

@app.get("/")
async def root():
    return "!Hola FastAPI"

@app.get("/url")
async def url():
    return {"url_curso": "https://mouredev.com/python"}