from fastapi import FastAPI
from api.routes import router  # Import API routes
import uvicorn
import os

# Initialize FastAPI app
app = FastAPI(title="My Full-Stack Project", version="1.0.0")

# Include routes
app.include_router(router)

# Root route
@app.get("/")
def read_root():
    return {"message": "Welcome to the API"}

# Start the app when running this file
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=int(os.getenv("PORT", 8000)))
