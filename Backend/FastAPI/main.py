from fastapi import FastAPI

# Importaciones de Routers
from routers import products
from routers import user

# Importaciones de recursos estaticos
from fastapi.staticfiles import StaticFiles


app = FastAPI()

# Routers
app.include_router(products.router)
app.include_router(user.router)

# Recursos estaticos
app.mount("/static",StaticFiles(directory="static"),name="static")
# Link para verlo en el explorador: http://127.0.0.1:8000/static/images/Logo.png

@app.get("/")
async def root():
    return "!Hola FastAPI"

@app.get("/url")
async def url():
    return {"url_curso": "https://mouredev.com/python"}