from fastapi import APIRouter, HTTPException
from app.database import news_collection
from typing import List

router = APIRouter()

@router.get("/")
async def get_all_news(limit: int = 20):
    cursor = news_collection.find().sort("scraped_at", -1)
    articles = await cursor.to_list(length=limit)
    # Convert MongoDB _id to string for the frontend
    for article in articles:
        article["_id"] = str(article["_id"])
    return articles