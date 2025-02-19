from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt
from passlib.context import CryptContext
from fastapi import FastAPI, HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer
from typing import List
import pika
import json


app = FastAPI()

SECRET_KEY = "f8a42ab8fa9a4b70a2e61e6d1df74d1b2b2f98703934950fe700f76bba6d6849"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

def on_request(ch, method, properties, body):
    user_id = json.loads(body)["user_id"]
    
    
    user_data = {"user_id": user_id, "name": "John Doe"}
    
    
    ch.basic_publish(exchange='',
                     routing_key=properties.reply_to,
                     properties=pika.BasicProperties(
                         correlation_id=properties.correlation_id),
                     body=str(user_data))  # Responder con los datos del usuario

    ch.basic_ack(delivery_tag=method.delivery_tag)

connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()

channel.queue_declare(queue='user_queue')

channel.basic_consume(queue='user_queue', on_message_callback=on_request)

print("Awaiting RPC requests")
channel.start_consuming()

# Función para encriptar la contraseña
def get_password_hash(password: str):
    return pwd_context.hash(password)

# Función para verificar si una contraseña coincide
def verify_password(plain_password: str, hashed_password: str):
    return pwd_context.verify(plain_password, hashed_password)

# Función para crear un token JWT
def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

# Función para verificar un token JWT
def verify_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        return None

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

# Función para obtener el usuario a partir del token
def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=401,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = verify_token(token)
        if payload is None:
            raise credentials_exception
        username = payload.get("sub")
        if username is None:
            raise credentials_exception
        return username
    except JWTError:
        raise credentials_exception
    
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

def create_access_token(data: dict, expires_delta: timedelta = timedelta(hours=1)):
    to_encode = data.copy()
    to_encode.update({"exp": datetime.utcnow() + expires_delta})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class UserProfileUpdate(BaseModel):
    full_name: Optional[str] = None
    email: Optional[EmailStr] = None
    new_password: Optional[str] = None  

    
class UserLogin(BaseModel):
    username: str
    password: str
    
class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str
    full_name: Optional[str] = None

users_db = [
    {
        "username": "john_doe",
        "email": "john@example.com",
        "password": get_password_hash("securepassword123")  # Contraseña encriptada
    }
]

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

@app.post("/registrar")
async def register_user(user: UserCreate):
    
    for existing_user in users_db:
        if existing_user["email"] == user.email:
            raise HTTPException(status_code=400, detail="Email already registered")
    
    
    users_db.append(user.dict())
    
    return {"message": "User registered successfully", "user": user.username}

@app.post("/autenticar")
async def login_for_access_token(form_data: UserLogin):
    user = None
    for existing_user in users_db:
        if existing_user["username"] == form_data.username:
            user = existing_user
            break
    
    if not user or not verify_password(form_data.password, user["password"]):
        raise HTTPException(
            status_code=401,
            detail="Invalid username or password"
        )

    
    access_token = create_access_token(
        data={"sub": user["username"]}
    )
    return {"access_token": access_token, "token_type": "bearer"}

@app.put("/actualizar")
async def update_profile(
    user_update: UserProfileUpdate, 
    current_user: str = Depends(get_current_user), 
    old_password: Optional[str] = None
):
    # Buscar al usuario en la "base de datos"
    user = next((user for user in users_db if user["username"] == current_user), None)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # Verificar si la nueva contraseña es válida
    if user_update.new_password:
        if not old_password or not verify_password(old_password, user["password"]):
            raise HTTPException(status_code=400, detail="Old password is incorrect")
        
        # Encriptar la nueva contraseña y actualizarla
        user["password"] = get_password_hash(user_update.new_password)
    
    # Actualizar otros detalles si se proporcionan
    if user_update.full_name:
        user["full_name"] = user_update.full_name
    if user_update.email:
        user["email"] = user_update.email

    return {"message": "Profile updated successfully", "user": user}