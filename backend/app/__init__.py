from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config import settings

def create_app():
    app = FastAPI(
        title="Algomatics API",
        description="API for Algomatics - Math and Algorithms Teaching Platform",
        version="0.1.0"
    )

    # CORS setup to allow requests from Wix frontend
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.CORS_ORIGINS,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # Import and include routers
    from app.auth.routes import router as auth_router
    from app.algorithms.routes import router as algorithms_router
    from app.data_structures.routes import router as data_structures_router
    from app.math.routes import router as math_router
    from app.progress.routes import router as progress_router

    # Include routers
    app.include_router(auth_router, prefix="/api/auth", tags=["Authentication"])
    app.include_router(algorithms_router, prefix="/api/algorithms", tags=["Algorithms"])
    app.include_router(data_structures_router, prefix="/api/data-structures", tags=["Data Structures"])
    app.include_router(math_router, prefix="/api/math", tags=["Math"])
    app.include_router(progress_router, prefix="/api/progress", tags=["User Progress"])

    @app.get("/api/health", tags=["Health"])
    async def health_check():
        return {"status": "ok"}

    return app