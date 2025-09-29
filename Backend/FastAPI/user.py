from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

app = FastAPI()

# Entidad User
class User(BaseModel):
    id: int
    name: str
    surname: str
    url: str
    age: int

users_list = [
    User(id=1, name="Andy", surname="Gomez", url="https://moure.dev", age=36),
    User(id=2, name="Rougs", surname="Mont", url="https://Rougs.com", age=35),
    User(id=3, name="Any", surname="Gomez", url="https://Ani.es", age=27),
]


@app.get("/usersjson")
async def usersjson():
    return [
        {"name": "Andy", "surname": "Gomez", "url": "https://moure.dev", "age": 36},
        {"name": "Rougs", "surname": "Mont", "url": "https://Rougs.com", "age": 35},
        {"name": "Any", "surname": "Gomez", "url": "https://Ani.es", "age": 27},
    ]
def search_user(id: int):
    users = filter(lambda user: user.id ==id, users_list)
    try:                
        return list(users)[0]
    except:
        return {"Error!":"No se a encontrado el usuario"}

# Path
@app.get("/users")
async def users():
    return users_list

# Endpoint para llamar a usuario por id
@app.get("/user/{id}")
async def user(id:int):
    return search_user(id)

# Query
@app.get("/userquery")
async def user(id:int):
    return search_user(id)
    

# Post
@app.post("/user/",response_model=User, status_code=201)
async def user(user: User):
    if type(search_user(user.id)) == User:
        raise HTTPException(status_code= 409, detail="Usuario ya existe")        
    else:
        users_list.append(user)
        return user

# Put
@app.put("/user/",response_model=User, status_code=200)
async def user(user:User):

    found = False

    for index, saved_user in enumerate(users_list):
        if saved_user.id == user.id:
            users_list[index] = user
            found = True
            break

    if not found:
        raise HTTPException(status_code=404, detail="No se a actualizado el usuario")
    
    return user

# Delete
@app.delete("/user/{id}",status_code=200)
async def user(id:int):

    found = False

    for index, saved_user in enumerate(users_list):
        if saved_user.id == id:
            del users_list[index]
            found = True                    
            break
            
    if not found:
        raise HTTPException(status_code=404, detail=f"El usuario con ID {id} no fue encontrado.")
    return {"message": "Usuario eliminado con éxito"}
