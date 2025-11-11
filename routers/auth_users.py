"""
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import BaseModel
import jwt
from jwt.exceptions import  InvalidTokenError
from pwdlib import PasswordHash
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from datetime import *

ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 1
SECRET_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyfQ.SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c"
password_hash = PasswordHash.recommended()


router = APIRouter(
    prefix="/auth_users",
    tags=["auth_users"]
)
oauth2=OAuth2PasswordBearer(tokenUrl="login")

class User(BaseModel):
    username: str
    full_name: str
    email: str
    disabled: bool

class UserDB(User):
    password: str

users_db = {
    "johndoe": {
        "username": "johndoe",
        "full_name": "John Doe",
        "email": "Jhon@gmail.com",
        "disabled": False,
        "password": "12345"
    },
    "alice": {
        "username": "alice",
        "full_name": "Alice Wonderson",
        "email": "alice@gmail.com",
        "disabled": True,
        "password": "67890"
    }
}


@router.post("/login")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
   user = users_db.get(form.username)
   if user:
        if password_hash.verify(form.pasword, user["password"]):
            expire=datetime.now(datetime.timezone.utc)+timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
            acces_token={"sub":user.username, "exp": expire}
            token = jwt.encode(acces_token, SECRET_KEY, algorithm=ALGORITHM)
            return {"access_token": token, "token_type": "bearer"}
    
    raise HTTPException(status_code=400, detail="Incorrect username or password")

"""


from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel, EmailStr
import jwt
from jwt.exceptions import InvalidTokenError
from pwdlib import PasswordHash
from datetime import datetime, timedelta, timezone

ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 1
SECRET_KEY = "tu_clave_secreta_muy_segura_y_larga_aqui_cambiar_en_produccion"
password_hash = PasswordHash.recommended()

router = APIRouter(
    prefix="/auth_users",
    tags=["auth_users"]
)
oauth2 = OAuth2PasswordBearer(tokenUrl="login")

class User(BaseModel):
    username: str
    full_name: str
    email: str
    disabled: bool

class UserDB(User):
    password: str

class UserRegister(BaseModel):
    username: str
    full_name: str
    email: EmailStr
    password: str

# Contraseñas hasheadas (ejemplo con "12345" y "67890")
users_db = {
    "johndoe": {
        "username": "johndoe",
        "full_name": "John Doe",
        "email": "Jhon@gmail.com",
        "disabled": False,
        "password": password_hash.hash("12345")
    },
    "alice": {
        "username": "alice",
        "full_name": "Alice Wonderson",
        "email": "alice@gmail.com",
        "disabled": True,
        "password": password_hash.hash("67890")
    }
}

@router.post("/register", status_code=status.HTTP_201_CREATED)
async def register(user_data: UserRegister):
    # Verificar si el usuario ya existe
    if user_data.username in users_db:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username already registered"
        )
    
    # Verificar si el email ya existe
    for user in users_db.values():
        if user["email"] == user_data.email:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Email already registered"
            )
    
    # Crear nuevo usuario con contraseña hasheada
    new_user = {
        "username": user_data.username,
        "full_name": user_data.full_name,
        "email": user_data.email,
        "disabled": False,
        "password": password_hash.hash(user_data.password)
    }
    
    # Añadir usuario a la base de datos
    users_db[user_data.username] = new_user
    
    # Retornar usuario sin la contraseña
    return {
        "username": new_user["username"],
        "full_name": new_user["full_name"],
        "email": new_user["email"],
        "disabled": new_user["disabled"]
    }

@router.post("/login")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = users_db.get(form_data.username)
    
    if user:
        # Verificar: contraseña en texto plano vs hash almacenado
        if password_hash.verify(form_data.password, user["password"]):
            expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
            access_token = {"sub": user["username"], "exp": expire}
            token = jwt.encode(access_token, SECRET_KEY, algorithm=ALGORITHM)
            return {"access_token": token, "token_type": "bearer"}
    
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Incorrect username or password",
        headers={"WWW-Authenticate": "Bearer"}
    )