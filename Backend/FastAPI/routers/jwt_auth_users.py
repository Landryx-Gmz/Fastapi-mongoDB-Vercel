# Intalamos esta libreria de criptogracia 
# pip install pyjwt
# pip install "passlib[bcrypt]"


from fastapi import APIRouter, Depends,status,HTTPException
from pydantic import BaseModel
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

# Importatamos jwt Y passlib para encriptar
import jwt
from passlib.context import CryptContext
from jose import JWTError, jwt

# Importamos datetime y timedelta para el tiempo de expiracion de token
from datetime import datetime, timedelta , timezone


# Detalles de creacion de  token
ALGORITHM = "HS256"
ACCESS_TOKEN_DURATION = 5
SECRET = "asdiqedfsdkeijasodimomveomcovmeosdajsdfao4emvosdmoj390342rmfasdl"

router = APIRouter(
    prefix="/jwtauth",
    tags=["jwtauth"],
    responses={status.HTTP_404_NOT_FOUND:{"message":"No encontrado"}}
)
oauth2 = OAuth2PasswordBearer(tokenUrl="login")

# Definimos la variable de encriptacion
crypt =  CryptContext(schemes=["bcrypt"], deprecated="auto")


class User(BaseModel):
    username: str
    full_name: str
    email: str
    disabled: bool

class UserDB(User):
    password: str

# Base de datos
users_db ={
    "Andy":{
        "username": "Andy",
        "full_name": "Andy Gómez",
        "email": "andy@mail.es",
        "disabled": False,
        "password": "$2a$12$NzrpHUIyTnD91f1IU71ANOJYusAkK51AF8dsJLrpfV1fIjt6GuKlm"
    },
    "Rougsh":{
        "username": "Rougsh",
        "full_name": "Ross Mont",
        "email": "rougsh@mail.es",
        "disabled": True,
        "password": "$2a$12$.9ncInL7ztZUJhc6VaW3/u3KhnGpn8/.gxRWicg4RcuyIyVoxTpJ."
    }
}

def search_user_db(username:str):
    if username in users_db:
        return UserDB(**users_db[username])

def search_user(username: str):
    if username in users_db:
        return User(**users_db[username])

async def auth_user(token: str = Depends(oauth2)):
    exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Credenciales de autenticacion invalidas",
        headers={"WWW-Authenticate": "Bearer"})

    try:
        username = jwt.decode(token, SECRET, algorithms=[ALGORITHM]).get("sub")
        if username is None:
            raise exception

    except JWTError:
        raise exception

    return search_user(username)

async def current_user(user: User = Depends(auth_user)):
    if user.disabled:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Usuario inactivo")

    return user

@router.post("/login")
async def login(form: OAuth2PasswordRequestForm = Depends()):
    # Usuario
    user_db = users_db.get(form.username)
    if not user_db:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="El usuario es incorrecto")
    user = search_user_db(form.username)

    # ----Forma de verificacion----
    # crypt.verify(form.password,user.password)#pasamos la contraseña original y la contraseña en BD


    # Password
    if not crypt.verify(form.password,user.password):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,detail="La contraseña es incorrecta")

    # Calculo de expiracion de token
        
    access_token = {"sub" : user.username,
                    "exp" : datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_DURATION)}
    
    return {"access_token": jwt.encode(access_token, SECRET, algorithm=ALGORITHM), "token_type": "bearer"}

@router.get("/users/me")
async def me(user: User = Depends(current_user)):
    return user