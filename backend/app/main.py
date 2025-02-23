from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .core.config import settings
from .api.v1.endpoints import algorithms, math_problems, users

app = FastAPI(
    title=settings.PROJECT_NAME,
    version=settings.VERSION,
    openapi_url=f"{settings.API_V1_STR}/openapi.json"
)

# Set up CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.BACKEND_CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(
    users.router,
    prefix=f"{settings.API_V1_STR}/users",
    tags=["users"]
)

app.include_router(
    algorithms.router,
    prefix=f"{settings.API_V1_STR}/algorithms",
    tags=["algorithms"]
)

app.include_router(
    math_problems.router,
    prefix=f"{settings.API_V1_STR}/math-problems",
    tags=["math-problems"]
)

@app.get("/")
async def root():
    return {
        "message": "Welcome to Math & DSA Learning Platform API",
        "version": settings.VERSION,
        "docs_url": "/docs"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)