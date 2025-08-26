import env
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import health, apis

from db.mysql import connect_mysql

# Load environment variables from .env file

app = FastAPI(
    title="Py Url Shortener API",
    description="URL shorteners take any URL and generates a short key for it. This short key can be used to redirect users to the specified long URL. This is extremely useful for marketting on twitter bluesky and other social network. In this challenge you will be implementing few core APIs required for a scalable URL shortener",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Configure this properly for production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(health.router, prefix="", tags=["health"])
app.include_router(apis.router, prefix="", tags=["apis"])

@app.on_event("startup")
async def startup_event():
    """Initialize database connection on startup"""
    await connect_mysql()

if __name__ == "__main__":
    import uvicorn
    import os
    host = os.getenv("HOST", "0.0.0.0")
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host=host, port=port)