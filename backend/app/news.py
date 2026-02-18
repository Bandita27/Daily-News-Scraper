from fastapi import APIRouter
from .database import news_collection
from .schemas import NewsArticle
from typing import List

router= APIRouter()

@router.get("/", response_model=List[NewsArticle])
async def get_news(category: str = "tech"):
    # MongoDB find command
    cursor = news_collection.find({"category": category})
    articles = await cursor.to_list(length=100)
    return articles

@router.post("/scrape-task")
async def save_scraped_data(articles: List[dict]):
    # Insert multiple records into MongoDB
    await news_collection.insert_many(articles)
    return {"status": "success", "count": len(articles)}
