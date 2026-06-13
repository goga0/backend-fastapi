from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Dict
from uuid import uuid4

app = FastAPI()

class Item(BaseModel):
    name: str
    description: str | None = None
    price: float
    in_stock: bool = True

db: Dict[str, Item] = {}

@app.post("/items/", status_code=201)
def create_item(item: Item):
    item_id = str(uuid4())
    db[item_id] = item
    return {"id": item_id, **item.dict()}

@app.get("/items/")
def list_items():
    return [{"id": k, **v.dict()} for k, v in db.items()]

@app.get("/items/{item_id}")
def get_item(item_id: str):
    item = db.get(item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    return {"id": item_id, **item.dict()}

@app.put("/items/{item_id}")
def update_item(item_id: str, updated: Item):
    if item_id not in db:
        raise HTTPException(status_code=404, detail="Item not found")
    db[item_id] = updated
    return {"id": item_id, **updated.dict()}

@app.delete("/items/{item_id}", status_code=204)
def delete_item(item_id: str):
    if item_id not in db:
        raise HTTPException(status_code=404, detail="Item not found")
    del db[item_id]
