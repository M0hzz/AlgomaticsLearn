# backend/app/main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse
import webbrowser
import threading
import time
import os
import sys

# Add the parent directory to the Python path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Import from the project's modules
from app.api.v1.api import api_router

# Your Wix site URL
WIX_SITE_URL = "https://arwajlokhandwala.wixstudio.com/my-site"  # Replace with your actual Wix site URL

app = FastAPI(
    title="Math & Algorithms Platform",
    description="Educational platform for mathematics and algorithms",
    version="0.1.0",
)

# CORS settings - make sure to include your Wix site domain
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # You can restrict this to your Wix domain for security
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Root endpoint that redirects to your Wix site
@app.get("/", response_class=RedirectResponse)
async def root():
    return WIX_SITE_URL

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