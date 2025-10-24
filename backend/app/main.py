# app/main.py
from fastapi import FastAPI, Depends
from sqlalchemy import text
from sqlalchemy.orm import Session
from .database import SessionLocal

app = FastAPI(title="Expense Tracker API")

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


app = FastAPI()

@app.get("/health")
def health(db: Session = Depends(get_db)):
    row = db.execute(text("SELECT DB_NAME() AS db, SUSER_NAME() AS login, GETDATE() AS now")).mappings().one()
    return {"status": "ok", **row}