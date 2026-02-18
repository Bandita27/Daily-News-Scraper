from pydantic import BaseModel
from datetime import datetime

class NewsArticle(BaseModel):
    title: str
    link:str
    source:str
    categoty:str
    scraped_at: datetime