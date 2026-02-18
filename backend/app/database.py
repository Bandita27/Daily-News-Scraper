import motor.motor_asyncio
import os
from dotenv import load_dotenv

load_dotenv()

# 1. Get your MongoDB URI from .env or use a default
MONGO_DETAILS = os.getenv("MONGO_DETAILS", "mongodb://localhost:27017")

# 2. Initialize the Client
client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_DETAILS)

# 3. Define the 'db' variable (This was missing!)
db = client.news_database

# 4. Define your collections
news_collection = db.get_collection("news_links")
users_collection = db.get_collection("users") # Now 'db' is defined!