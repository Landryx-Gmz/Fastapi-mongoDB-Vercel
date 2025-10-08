# -------Ejemplo sin mongoDB-------
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

router = APIRouter(prefix="/user",
                    tags=["Users"],
                    responses={404: {"message":"No encontrado"}})

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
    User(id=3, name="Any", surname="Gomez", url="https://Ani.es", age=27),]


@router.get("/usersjson")
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
@router.get("/",status_code=200)
async def users():
    return users_list

# Endpoint para llamar a usuario por id
@router.get("/{id}")
async def user(id:int):
    return search_user(id)

# Query
@router.get("/userquery",response_model=User,status_code=200)
async def user(id:int):
    return search_user(id)
    

# Post
@router.post("/",response_model=User, status_code=201)
async def user(user: User):
    if type(search_user(user.id)) == User:
        raise HTTPException(status_code= 409, detail="Usuario ya existe")        
    else:
        users_list.append(user)
        return user

# Put
@router.put("/",response_model=User, status_code=200)
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
@router.delete("/{id}",status_code=200)
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
