from pydantic import BaseModel
from datetime import datetime
from pydantic import BaseModel, EmailStr

class UserCreate(BaseModel):
    username: str 
    email: EmailStr
    password: str

class UserLogin(BaseModel):
    email: EmailStr  # Make sure this says 'email', not 'username'
    password: str
class NewsArticle(BaseModel):
    title: str
    link:str
    source:str
    categoty:str
    scraped_at: datetime