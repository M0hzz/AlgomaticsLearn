import sys
import os
from fastapi import FastAPI
from api.auth import router as auth_router
from database import init_db
from fastapi.middleware.cors import CORSMiddleware

# Fix Import Errors (Ensure `backend/` is in sys.path)
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

app = FastAPI()

# Enable CORS so frontend can communicate with backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins (Change to specific domains in production)
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize Database on Startup
@app.on_event("startup")
def startup():
    init_db()

# Include API Routes
app.include_router(auth_router, prefix="/auth")

@app.get("/")
def home():
    return {"message": "Simple Authentication API"}
