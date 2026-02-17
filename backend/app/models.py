from sqlalchemy import Column, Integer, String, DateTime
from .database import Base
import datetime

class Article(Base):
    __tablename__="articles"
    id=Column(Integer, primary_key=True, index=True)
    title=Column(String)
    link=Column(String, unique=True)
    source=Column(String)
    category=Column(String)
    created_at=Column(DateTime,default=datetime.datetime.utcnow)