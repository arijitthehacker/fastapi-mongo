from bson import ObjectId
from fastapi import FastAPI, HTTPException
from fastapi.params import Depends
from pymongo import MongoClient 
from pydantic import BaseModel
import logging
from contextlib import asynccontextmanager

from models import CreateItem, ReadItem, UpdateItem, DeleteItem

logger = logging.getLogger("uvicorn.error")

async def connect_to_mongo():
    client = MongoClient("mongodb://localhost:27017")
    db = client["fastapi"]
    logger.debug("Connected to MongoDB:")
    return db

@asynccontextmanager
async def lifespan(app: FastAPI):
    await connect_to_mongo()
    yield
    logger.info("Disconnected from MongoDB")
    
app = FastAPI(lifespan=lifespan, debug=True)    


@app.post("/items/", response_model=CreateItem)
async def create_item(item: CreateItem):
    db = await connect_to_mongo()
    item_id = db["items"].insert_one(dict(item))
    created_item = db["items"].find_one({"_id": item_id.inserted_id})
    created_item['id'] = str(created_item['_id'])
    return created_item

@app.get("/items/{id}", response_model=ReadItem)
async def read_item(id: str):
    db = await connect_to_mongo()
    item = db["items"].find_one({"_id": ObjectId(id)})
    if not item:
        raise HTTPException(status_code=404, detail=f"Item {id} not found")
    return item