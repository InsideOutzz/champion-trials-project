from fastapi import FastAPI

from app.database import engine, Base
from app.routers import buses, reports, heatmap, users, developer_keys

# Create database tables
Base.metadata.create_all(bind=engine)

# Initialize API
app = FastAPI(
    title="Bus Crowd Meter API",
    description="Bus crowd reporting and user authentication",
    version="2.0.0"
)

# Register routers
app.include_router(users.router)
app.include_router(buses.router)
app.include_router(reports.router)
app.include_router(heatmap.router)
app.include_router(developer_keys.router)

print("\n========== DEVELOPER ROUTER DIAGNOSTIC ==========")

for route in app.routes:
    if "developer" in getattr(route, "path", ""):
        print("Path:", route.path)
        print("Methods:", getattr(route, "methods", None))

print("=================================================\n")



@app.get("/")
def home():
    return {
        "message": "Welcome to Bus Crowd Meter API!",
        "status": "running"
    }


@app.get("/health")
def health():
    return {"status": "healthy"}