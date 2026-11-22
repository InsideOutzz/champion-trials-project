from fastapi import FastAPI

from app.database import engine, Base
from app.routers import buses, reports, heatmap

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Bus Crowd Meter API",
    description="API for reporting and analyzing bus crowd levels",
    version="1.0.0"
)

app.include_router(buses.router)
app.include_router(reports.router)
app.include_router(heatmap.router)


@app.get("/")
def home():
    return {
        "message": "Welcome to Bus Crowd Meter API!",
        "status": "running"
    }


@app.get("/health")
def health():
    return {"status": "healthy"}