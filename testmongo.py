from fastapi import FastAPI
from pydantic import BaseModel
from motor.motor_asyncio import AsyncIOMotorClient
from bson import ObjectId
import os
from dotenv import load_dotenv

load_dotenv()  # Load environment variables from .env file
mongo_uri = os.getenv("MONGO_URI")  # Get the MongoDB URI from environment variables

client =AsyncIOMotorClient(mongo_uri)
db = client["euron"]
euron_data = db["euron_student"]

app = FastAPI()

class EuronData(BaseModel):
    name: str
    phone: int
    city: str
    course: str

@app.post("/euron_data/insert")
async def euron_data_insert(data: EuronData):
    result = await euron_data.insert_one(data.dict())
    return str(result.inserted_id)

@app.get("/euron_data/get_data")
async def get_euron_data():
    items = []
    cursor = euron_data.find({})
    async for document in cursor:
        document["_id"] = str(document["_id"])  # Convert ObjectId to string
        items.append(document)
    return items