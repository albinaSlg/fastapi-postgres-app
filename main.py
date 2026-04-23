from fastapi import FastAPI, HTTPException, status
from pydantic import BaseModel, ConfigDict
from typing import List
import os

from database import SessionLocal
import models

app = FastAPI()
db = SessionLocal()

class Item(BaseModel):
    id: int
    name: str
    description: str
    price: float
    on_offer: bool

    model_config = ConfigDict(from_attributes=True)

@app.get("/")
def root():
    return {
        "database_name": os.getenv("database_name"),
        "host_server": os.getenv("host_server"),
        "db_username": os.getenv("db_username")
    }

@app.get("/items", response_model=List[Item], status_code=200)
def get_all_items():
    return db.query(models.Item).all()

@app.get("/item/{item_id}", response_model=Item, status_code=status.HTTP_200_OK)
def get_an_item(item_id: int):
    item = db.query(models.Item).filter(models.Item.id == item_id).first()
    if item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return item

@app.post("/items", response_model=Item, status_code=status.HTTP_201_CREATED)
def create_an_item(item: Item):
    db_item = models.Item(
        id=item.id,
        name=item.name,
        description=item.description,
        price=item.price,
        on_offer=item.on_offer
    )
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

@app.put("/item/{item_id}", response_model=Item, status_code=status.HTTP_200_OK)
def update_an_item(item_id: int, item: Item):
    db_item = db.query(models.Item).filter(models.Item.id == item_id).first()
    if db_item is None:
        raise HTTPException(status_code=404, detail="Item not found")

    db_item.name = item.name
    db_item.description = item.description
    db_item.price = item.price
    db_item.on_offer = item.on_offer
    db.commit()
    db.refresh(db_item)
    return db_item

@app.delete("/item/{item_id}", status_code=status.HTTP_200_OK)
def delete_an_item(item_id: int):
    db_item = db.query(models.Item).filter(models.Item.id == item_id).first()
    if db_item is None:
        raise HTTPException(status_code=404, detail="Item not found")

    db.delete(db_item)
    db.commit()
    return {"message": "Item deleted successfully"}