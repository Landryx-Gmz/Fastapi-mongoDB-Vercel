from fastapi import APIRouter, HTTPException,status
from db.models.user import User
from db.client import db_client
from db.schemas.user import user_schema

router = APIRouter(prefix="/userdb",
                    tags=["userdb"],
                    responses={status.HTTP_404_NOT_FOUND:{"message":"No encontrado"}})

# Entidad User

users_list = []

@router.get("/",status_code=200)
async def users():
    return users_list

# Path
@router.get("/{id}")
async def user(id:int):
    return search_user(id)

# Query
@router.get("/",response_model=User,status_code=200)
async def user(id:int):
    return search_user(id)

def search_user(id: int):
    users = filter(lambda user: user.id ==id, users_list)
    try:                
        return list(users)[0]
    except:
        return {"Error!":"No se a encontrado el usuario"}
    

# Post/mongodb
@router.post("/",response_model=User, status_code=status.HTTP_201_CREATED)
async def user(user: User):

    # if type(search_user(user.id)) == User:
    #     raise HTTPException(status_code= 409, detail="Usuario ya existe")        
    # else:
    user_dict = dict(user)
    del user_dict["id"] #eliminamos el id para que mongo nos lo proporcione

    id= db_client.local.users.insert_one(user_dict).inserted_id # para acceder a mongo se hace con .local

    new_user = user_schema(db_client.local.users.find_one({"_id":id}))# el nombre de campo que crea mongo es _id


    return User(**new_user)

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
