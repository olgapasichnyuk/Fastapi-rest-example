from typing import List

from fastapi import FastAPI, Depends, HTTPException, status
from pydantic import BaseModel
from sqlalchemy import text
from sqlalchemy.orm import Session

from connect_db import get_db
from models import Item

app = FastAPI()


@app.get('/')
def read_root():
    return {"message": "all right!"}


@app.get('/api/healthchecker')
def healthchecker(db: Session = Depends(get_db)):
    try:
        res = db.execute(text("SELECT 1")).fetchone()

        if res is None:
            raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                                detail="Data base configurated incorrect")
        return {"message": "Welcome to FastAPI!"}

    except Exception:
        print(Exception)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                            detail="Error connection to DB")


class ResponseItem(BaseModel):
    id: int
    name: str
    size: int
    description: str

    class Config:
        orm_mode = True


@app.get('/items', response_model=List[ResponseItem])
async def get_items(db: Session = Depends(get_db)):
    items = db.query(Item).all()
    return items


@app.get('/items/{item_id}', response_model=ResponseItem)
async def get_item(item_id: int, db: Session = Depends(get_db)):
    item = db.query(Item).filter_by(id=item_id).first()
    if item is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="Not found")
    return item
