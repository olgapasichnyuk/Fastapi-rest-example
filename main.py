from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy import text
from sqlalchemy.orm import Session

from connect_db import get_db
from models import Item

app = FastAPI()


@app.get('/')
def read_root():
    return{"message": "all right!"}


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


@app.get('/items')
async def get_items(db: Session = Depends(get_db)):
    items = db.query(Item).all()
    return items

