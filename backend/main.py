from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
import httpx
from bs4 import BeautifulSoup

app = FastAPI()

# IMPORTANT: Keep CORS so React can connect
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

async def scrape_hacker_news():
    async with httpx.AsyncClient() as client:
        response = await client.get("https://news.ycombinator.com/")
    soup = BeautifulSoup(response.text, "html.parser")
    articles = []
    for item in soup.find_all("span", class_="titleline")[:15]:
        anchor = item.find("a")
        if anchor:
            articles.append({"title": anchor.text, "url": anchor["href"]})
    return articles

async def scrape_bbc_news():
    headers = {"User-Agent": "Mozilla/5.0"}
    async with httpx.AsyncClient() as client:
        response = await client.get("https://www.bbc.com/news", headers=headers)
    
    soup = BeautifulSoup(response.text, "html.parser")
    articles = []
    # Using a slightly broader selector to be safe
    headlines = soup.select('h2, h3')
    
    for h in headlines[:20]:
        parent_a = h.find_parent('a')
        if parent_a and parent_a.get('href'):
            link = str(parent_a.get('href'))
            if link.startswith('/'):
                link = f"https://www.bbc.com{link}"
            
            title = h.text.strip()
            if title and len(title) > 10: # Filter out short menu items
                articles.append({"title": title, "url": link})
    return articles

@app.get("/news") 
async def get_news(source: str = "hackernews"):
    if source == "bbc":
        data = await scrape_bbc_news()
    else:
        data = await scrape_hacker_news()
    return {"articles": data}