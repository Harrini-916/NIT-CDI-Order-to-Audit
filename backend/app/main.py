
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy import text
from sqlalchemy.orm import Session

from app.db.database import get_db

app = FastAPI(
    title="NIT CDI Order-to-Audit System",
    description="Order management, production, inventory, GST billing and audit system",
    version="1.0.0"
)

@app.get("/")
def home():
    return {
        "message": "Welcome to NIT CDI Order-to-Audit System",
        "status": "Backend is running"
    }

@app.get("/health")
def health_check():
    return {"status": "healthy"}

@app.get("/health/database")
def database_health(db: Session = Depends(get_db)):
    try:
        db.execute(text("SELECT 1"))
        return {
            "status": "connected",
            "database": "nit_cdi_order_audit"
        }
    except Exception:
        raise HTTPException(
            status_code=503,
            detail="Database connection failed"
        )
