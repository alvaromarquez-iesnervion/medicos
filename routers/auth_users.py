from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security.oauth2 import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel
from pwdlib import PasswordHash
from datetime import datetime, timedelta, timezone
import jwt
from jwt import PyJWTError

router = APIRouter(
    prefix="",
    tags=["auth_users"]
)
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 1
SECRET_KEY = "tkqVtL5cZk_vyWK5plrqHJn4zFm8lqhrnCNvEwbYDX0tljwSXe5eAtzd4oo_Ryxb"
password_hash = PasswordHash.recommended()

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
        "disabled": False,
        "password": "67890"
    },
    "alvaro":{
        
        "username": "alvaro",
        "full_name": "alvaro marquez",
        "email": "alvaro@gmail.com",
        "disabled": False,
        "password": "$argon2id$v=19$m=65536,t=3,p=4$VFmBZprJLIXw4twGRmQBXw$xmmkghef5yyEQipICyeNrSYo/XONTx8+fNG3g+WpMzA"
        
    }
}

@router.post("/register", status_code=201)
def register(usuario: UserDB):
    if usuario.username not in users_db:
        hashed_password = password_hash.hash(usuario.password)
        usuario.password = hashed_password
        users_db[usuario.username] = usuario
        return usuario
    raise HTTPException(status_code=400,detail="El usuario ya existe")
    

@router.post("/login")

@router.post("/login")
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user_db = users_db.get(form_data.username)
    if user_db:
        user = UserDB(**user_db)  
        try:
            if password_hash.verify(form_data.password, user.password):  
                expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
                access_token = {"sub": user.username, "exp": expire}  
                token = jwt.encode(access_token, SECRET_KEY, algorithm=ALGORITHM)
                return {"access_token": token, "token_type": "bearer"}
        except:
            raise HTTPException(status_code=400, detail="error en la autenticacion")
    raise HTTPException(status_code=401, detail="Incorrect username or password")



async def authentication(token:str = Depends(oauth2)):
    try:
        username=jwt.decode(token, SECRET_KEY, algorithm=ALGORITHM).get("sub")
        if username is None:
            raise HTTPException(status_code=401, detail="Invalid autenitcation credentials", headers={"WWW-Authenticate": "Bearer"})
        
    except PyJWTError:
        raise HTTPException(status_code=401, detail="Invalid autenitcation credentials", headers={"WWW-Authenticate": "Bearer "})

    user=User(**users_db.get(username))
    if user.disabled:
        raise HTTPException(status_code=400, detail="Inactive user")
    return user