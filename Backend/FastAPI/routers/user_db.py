from fastapi import APIRouter, HTTPException,status
from db.models.user import User
# Importamos la base de datos de monogdb desde client.py
from db.client import db_client
from db.schemas.user import user_schema, users_schema
# Importaciones para tipo de id que ustiliza mongodb
from bson import ObjectId

router = APIRouter(prefix="/userdb",
                    tags=["userdb"],
                    responses={status.HTTP_404_NOT_FOUND:{"message":"No encontrado"}})


@router.get("/",response_model=list[User],status_code=200)
async def users():
    return users_schema(db_client.users.find())

# Path
@router.get("/{id}")
async def user(id:str):
    return search_user("_id", ObjectId(id))

# Query
@router.get("/",status_code=200)
async def user(id:str):
    return search_user("_id",ObjectId(id))


    

# Post/mongodb
@router.post("/",response_model=User, status_code=status.HTTP_201_CREATED)
async def user(user: User):

    if type(search_user("email",user.email)) == User:
        raise HTTPException(
            status_code= status.HTTP_404_NOT_FOUND, detail="Usuario ya existe")

    user_dict = dict(user)
    del user_dict["id"] #eliminamos el id para que mongo nos lo proporcione

    id= db_client.users.insert_one(user_dict).inserted_id 

    new_user = user_schema(db_client.users.find_one({"_id":id}))# el nombre de campo que crea mongo es _id

    return User(**new_user)

# Put
@router.put("/{id}",response_model=User)
async def user(user:User):
    user_dict = dict(user)
    del user_dict["id"]

    try:
        

        db_client.users.find_one_and_replace(
            {"_id":ObjectId(user.id)}, user_dict)
    
    except:
        return {"error":"No se a actualizado el usuario"}

    return search_user("_id",ObjectId(user.id))

# Delete
@router.delete("/{id}",status_code=status.HTTP_204_NO_CONTENT)
async def user(id:str):

    found = db_client.users.find_one_and_delete({"_id":ObjectId(id)})
            
    if not found:
        return {"message": "Usuario eliminado con éxito"}

    

def search_user(field: str, key):
    
    try:
        user = db_client.users.find_one({field: key})            
        return User(**user_schema(user))
    except:
        return {"Error!":"No se a encontrado el usuario"}
