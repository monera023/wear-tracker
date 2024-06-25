from typing import List, Optional

from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware

from server.Constants import WearItem, WearItemTrackingEntry
from server.wear_service import WearService

app = FastAPI()

DB_NAME = "wear-tracker.db"
wear_service = WearService(DB_NAME)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def home():
    return "OK"

@app.post("/v1/addWearItem")
async def insert_wear(items: List[WearItem]):
    print(f"Got wear items:: {len(items)}")
    wear_service.add_wear_items(items)
    return items

@app.get("/v1/fetchAllWearItems")
async def fetch_wear_items():
    print(f"In fetch_wear_items")
    items = wear_service.fetch_wear_items()
    return items

@app.post("/v1/addWearTracking")
async def add_wear_tracking_entry(items: List[WearItemTrackingEntry]):
    print(f"In add_wear_tracking_entry for:: {len(items)}")
    wear_service.add_wear_items_tracking(items)
    return items

@app.get("/v1/fetchWearItemTracking/{wear_item}")
async def fetch_wear_item_tracking(wear_item):
    print(f"In fetch_wear_item_tracking for :: {wear_item}")
    output = wear_service.fetch_wear_item_tracking(wear_item)
    return output

@app.get("/v1/fetchWearItemsWithTracking")
async def fetch_items_with_tracking():
    print(f"In fetch_items_with_tracking")
    output = wear_service.fetch_wear_items_with_tracking()
    return output

@app.get("/v1/search")
async def search_wear_items(name: Optional[str] = Query(None, description="Search terms"),
                            color: Optional[str] = Query(None, description="Color of item")):
    print(f"In search_wear_items for {name}...{color}")
    query_param_dict = {'name': name, 'color': color}
    output = wear_service.search_wear_items(query_param_dict)
    return output

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, port=8000)