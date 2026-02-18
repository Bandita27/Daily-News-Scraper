import httpx
from bs4 import BeautifulSoup
from app.database import news_collection
from datetime import datetime

# Define it ONLY ONCE
async def run_news_scraper():
    url = "https://news.ycombinator.com/"
    
    # Initialize links as an empty list so it's always defined
    links = [] 
    
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(url)
            response.raise_for_status()
            
        soup = BeautifulSoup(response.text, "html.parser")
        # Select the news titles
        links = soup.select(".titleline > a")
        
        if not links:
            print("No links found.")
            return

        for link in links[:20]:
            article_data = {
                "title": link.get_text(),
                "link": link["href"],
                "source": "Hacker News",
                "category": "tech",
                "scraped_at": datetime.utcnow()
            }
            
            # Upsert into MongoDB (Updates if link exists, inserts if not)
            await news_collection.update_one(
                {"link": article_data["link"]},
                {"$set": article_data},
                upsert=True
            )
            
        print(f"Successfully scraped {len(links[:20])} articles.")
        
    except Exception as e:
        print(f"Scraping failed: {e}")