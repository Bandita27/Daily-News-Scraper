from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional

class NewsArticle(BaseModel):
    title: str
    link: str
    source: str
    category: str
    scraped_at: datetime = Field(default_factory=datetime.utcnow)

    class Config:
        json_schema_extra = {
            "example": {
                "title": "New AI Discovery",
                "link": "https://techcrunch.com/...",
                "source": "TechCrunch",
                "category": "technology"
            }
        }