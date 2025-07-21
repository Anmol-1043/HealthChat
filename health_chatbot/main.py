from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import health_advice, user_profile
from database.database import engine
from models import models as db_models

# Create database tables
db_models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Health Advice Chatbot API",
    description="A FastAPI backend for providing personalized health advice based on user data",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8000", "http://127.0.0.1:8000"],  # Django frontend URLs
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(health_advice.router, prefix="/api", tags=["health-advice"])
app.include_router(user_profile.router, prefix="/api", tags=["user-profile"])

@app.get("/")
async def root():
    return {"message": "Health Advice Chatbot API is running!"}

@app.get("/health")
async def health_check():
    return {"status": "healthy"} 