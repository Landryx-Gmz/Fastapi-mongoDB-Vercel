from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

# Entidad User
class User(BaseModel):
    name: str
    surname: str
    url: str
    age: int

users_list = [
    User(name="Andy", surname="Gomez", url="https://moure.dev", age=36),
    User(name="Rougs", surname="Mont", url="https://Rougs.com", age=35),
    User(name="Any", surname="Gomez", url="https://Ani.es", age=27),
]


@app.get("/usersjson")
async def usersjson():
    return [
        {"name": "Andy", "surname": "Gomez", "url": "https://moure.dev", "age": 36},
        {"name": "Rougs", "surname": "Mont", "url": "https://Rougs.com", "age": 35},
        {"name": "Any", "surname": "Gomez", "url": "https://Ani.es", "age": 27},
    ]


@app.get("/users")
async def users():
    return users_list