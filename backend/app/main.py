# backend/app/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import webbrowser
import threading
import time
import os
import sys

# Add the parent directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Import database and models for initialization
from backend.app.database import engine
from backend.app.models import user

# Create database tables
user.Base.metadata.create_all(bind=engine)

# Import API router
from backend.app.api.v1.api import api_router

# Your Wix site URL
WIX_SITE_URL = "https://your-wix-site-url.com"  # Replace with your actual Wix site URL

app = FastAPI(
    title="Math & Algorithms Platform",
    description="Educational platform for mathematics and algorithms",
    version="0.1.0",
)

# CORS settings
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # You can restrict this to your Wix domain for security
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Root endpoint that redirects to your Wix site
@app.get("/")
async def root():
    return {"message": "Welcome to Math & Algorithms API"}

# Include API router
app.include_router(api_router, prefix="/api/v1")

# Function to open the Wix site in browser
def open_browser():
    # Wait for server to start
    time.sleep(2)
    # Open the Wix site in the default browser
    webbrowser.open(WIX_SITE_URL)
    print(f"Opened Wix site: {WIX_SITE_URL}")

if __name__ == "__main__":
    import uvicorn

    # Start a thread to open the browser
    threading.Thread(target=open_browser).start()

    # Run the FastAPI server
    uvicorn.run(app, host="0.0.0.0", port=8000)