from fastapi import FastAPI, HTTPException, Depends
from typing import List
from pydantic import BaseModel
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from datetime import datetime, timedelta
import uvicorn
import pika

app = FastAPI()

SECRET_KEY = "e7745733f36a4d17894f15cb6c25bc9d3fbbb21a77aab60bfcad3f4d8ed5a69d"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# Dependencia para obtener el token JWT
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def send_message_to_user_service(user_id):
    connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
    channel = connection.channel()

    channel.queue_declare(queue='user_queue')

    message = {"user_id": user_id}
    channel.basic_publish(exchange='',
                          routing_key='user_queue',
                          body=str(message))  

    print(f"Sent message: {message}")
    connection.close()
    
class PublicationCreate(BaseModel):
    title: str
    content: str


publications_db = []


users_db = [
    {"user_id": 1, "username": "john_doe", "name": "John Doe"},
    {"user_id": 2, "username": "jane_doe", "name": "Jane Doe"}
]

# Endpoint para crear una nueva publicación
@app.post("/crear")
async def create_post(publication: PublicationCreate, user_id: int):
   
    user = next((user for user in users_db if user["user_id"] == user_id), None)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    
    new_publication = {
        "user_id": user_id,
        "user_name": user["name"],
        "title": publication.title,
        "content": publication.content
    }
    
    
    publications_db.append(new_publication)

    return {"message": "Post created successfully", "post": new_publication}

@app.get("/user/{user_id}/posts", response_model=List[dict])
async def list_user_posts(user_id: int):
    # Filtrar las publicaciones por el user_id
    user_posts = [post for post in publications_db if post["user_id"] == user_id]

    if not user_posts:
        raise HTTPException(status_code=404, detail="No posts found for this user")

    return user_posts

def verify_token(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=401, detail="Could not validate credentials"
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        user_id: int = payload.get("sub")
        if user_id is None:
            raise credentials_exception
        return user_id  # Devuelve el user_id extraído del token
    except JWTError:
        raise credentials_exception

# Modelo para las publicaciones
class Post(BaseModel):
    post_id: int
    user_id: int
    title: str
    content: str

# Endpoint para eliminar una publicación
@app.delete("/posts/{post_id}")
async def delete_post(post_id: int, user_id: int = Depends(verify_token)):
    
    post_to_delete = next((post for post in publications_db if post["post_id"] == post_id), None)
    
    if post_to_delete is None:
        raise HTTPException(status_code=404, detail="Post not found")
    
    
    if post_to_delete["user_id"] != user_id:
        raise HTTPException(status_code=403, detail="Not authorized to delete this post")
    
    
    publications_db.remove(post_to_delete)
    
    return {"message": "Post deleted successfully"}