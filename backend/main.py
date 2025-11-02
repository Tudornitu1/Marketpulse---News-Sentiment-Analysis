from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import os
from dotenv import load_dotenv
from bson import ObjectId
from pymongo import MongoClient
import certifi
from datetime import datetime

load_dotenv()

MONGODB_URI = os.getenv("MONGODB_URI")
if not MONGODB_URI:
    raise RuntimeError("MONGODB_URI not set")

client = MongoClient(MONGODB_URI, tlsCAFile=certifi.where())
db = client["marketpulse_db"]

app = FastAPI()

# allow requests from your frontend dev server
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # adjust for prod
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def serialize_doc(doc):
    # convert ObjectId and datetimes
    doc = dict(doc)
    _id = doc.pop("_id", None)
    if _id is not None:
        doc["id"] = str(_id)
    for k, v in list(doc.items()):
        if isinstance(v, datetime):
            doc[k] = v.isoformat()
    return doc

@app.get("/api/news", response_model=List[dict])
def list_news(limit: int = 50, skip: int = 0):
    cursor = db.news.find().sort("date", -1).skip(skip).limit(limit)
    return [serialize_doc(d) for d in cursor]

@app.get("/api/news/{item_id}", response_model=dict)
def get_news(item_id: str):
    doc = db.news.find_one({"_id": ObjectId(item_id)})
    if not doc:
        raise HTTPException(status_code=404, detail="Not found")
    return serialize_doc(doc)

@app.get("/api/stocks", response_model=List[dict])
def list_stocks(symbol: Optional[str] = None, limit: int = 100):
    q = {}
    if symbol:
        q["symbol"] = symbol
    cursor = db.stocks.find(q).sort("Date", -1).limit(limit)
    return [serialize_doc(d) for d in cursor]