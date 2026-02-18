from fastapi import FastAPI
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from .controller import router as news_router
from .engine import run_news_scraper

@asynccontextmanager
async def lifespan(app: FastAPI):
    scheduler = AsyncIOScheduler()
    # Runs the scraper once on startup, then every 24 hours
    scheduler.add_job(run_news_scraper, 'interval', hours=24)
    scheduler.start()
    yield
    scheduler.shutdown()

app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(news_router, prefix="/api/v1/news", tags=["News"])

@app.get("/")
async def root():
    return {"message": "Daily News Scraper API is online"}