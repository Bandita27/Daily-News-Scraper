import os
from dotenv import load_dotenv
# Corrected spelling: 'asyncio' NOT 'asynchio'
from motor.motor_asyncio import AsyncIOMotorClient 

load_dotenv()

# Define MONGO_DETAILS before using it
MONGO_DETAILS = os.getenv("DATABASE_URL")

if not MONGO_DETAILS:
    MONGO_DETAILS = "mongodb://localhost:27017"

# Now use the variable
client = AsyncIOMotorClient(MONGO_DETAILS)
database = client.news_db
news_collection = database.get_collection("articles")