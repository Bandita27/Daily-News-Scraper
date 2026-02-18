from fastapi import APIRouter, HTTPException
from app.database import news_collection, users_collection
from typing import List, Optional
from .engine import run_news_scraper # Ensure this import is correct
from typing import List, Optional  # Add Optional to your imports
from app.auth import hash_password, verify_password, create_access_token


from app.schemas import UserCreate, UserLogin # Import the schemas

router = APIRouter()

@router.post("/signup")
async def signup(user_data: UserCreate): # Use the schema here
    # Change user_data["email"] to user_data.email
    existing_user = await users_collection.find_one({"email": user_data.email})
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    new_user = {
        "email": user_data.email,
        "password": hash_password(user_data.password)
    }
    await users_collection.insert_one(new_user)
    return {"message": "User created successfully"}

@router.post("/login")
async def login(login_data: UserLogin):
    # This line looks for 'email'. If your JSON sends 'username', this returns None.
    user = await users_collection.find_one({"email": login_data.email}) 
    
    if not user:
        print("User not found in DB") # Debugging hint
        raise HTTPException(status_code=401, detail="Invalid credentials")
        
    if not verify_password(login_data.password, user["password"]):
        print("Password mismatch") # Debugging hint
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    token = create_access_token({"sub": user["email"]})
    return {"access_token": token, "token_type": "bearer"}

@router.get("/")
async def get_all_news(
    limit: int = 20, 
    search: Optional[str] = None,   # This tells Pylance None is okay
    category: Optional[str] = None  # This tells Pylance None is okay
):
    query = {}
    if search:
        query["title"] = {"$regex": search, "$options": "i"}
    if category and category != "All":
        query["category"] = category.lower()

    # The rest of your logic remains the same...
    cursor = news_collection.find(query).sort("scraped_at", -1)
    articles = await cursor.to_list(length=limit)
    
    for article in articles:
        article["_id"] = str(article["_id"])
    return articles

@router.post("/scrape")
async def trigger_scrape():
    try:
        await run_news_scraper()
        return {"message": "Scraping completed successfully"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

