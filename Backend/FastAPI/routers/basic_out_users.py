from fastapi import FastAPI, status, Depends, HTTPException #importamos dependecias de fastapi y httpexeptions
from pydantic import BaseModel

# Importamos el modulo de autenticacion de fastapi (protocolo de autenticacion), (forma en la que el backen recibe el password en nuestro sistema)
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

app = FastAPI()

# Instancia de sistema de autenticacion
oaut2 = OAuth2PasswordBearer(tokenUrl="login")

# Modelado de usuarios
class User(BaseModel):
    username: str
    full_name: str
    email: str
    disable: bool

# Modelado de usuario de base de datos
class UserDB(User):
    password: str


# Base de datos
users_db ={
    "Andy":{
        "username": "Andy",
        "full_name": "Andy Gómez",
        "email": "andy@mail.es",
        "disable": False,
        "password": "123456"
    },
    "Rougsh":{
        "username": "Rougsh",
        "full_name": "Ross Mont",
        "email": "rougsh@mail.es",
        "disable": True,
        "password": "654321"
    }
}

# Funcion para buscar por username
def search_user_db(username: str):
    if username in users_db:
        return UserDB(**users_db[username])

def search_user(username: str):
    if username in users_db:
        return User(**users_db[username])

# Criterio de dependencia 
async def current_user(token: str = Depends(oaut2)):
    user = search_user(token)
    if not user:
        raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Credenciales de autenticacion invalidas", 
                headers={"WWW-Authenticate": "Bearer"})
    if user.disable:
        raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Usuario inactivo")
    return user

# Endpoint de autenticaion

@app.post("/login")
async def login(form: OAuth2PasswordRequestForm = Depends()):
    user_db = users_db.get(form.username)
    if not user_db:
        raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST, 
                detail="El usuario no es correcto")
    user = search_user_db(form.username)
    if not form.password == user.password:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="La contraseña no es correcta")
    return {"access_token": user.username, "token_type": "bearer"}

@app.get("/users/me")
async def me(user: User = Depends(current_user)):
    return user
