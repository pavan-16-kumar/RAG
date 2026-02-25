from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.config.settings import settings
from src.api.routes import router as api_router
from src.utils.logger import logger

def create_app() -> FastAPI:
    """Factory function to create and configure the FastAPI application."""
    
    logger.info(f"Initializing FastAPI App: {settings.app_name} ({settings.app_env})")
    
    app = FastAPI(
        title=settings.app_name,
        description="A scalable and industry-ready Retrieval-Augmented Generation API based on LangChain.",
        version="1.0.0",
        debug=settings.app_debug
    )
    
    # Configure CORS middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"], # In production, restrict this to specific origins
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    
    # Register core routers
    app.include_router(api_router)
    
    @app.on_event("startup")
    async def startup_event():
        logger.info("FastAPI Application fully started.")
        
    @app.on_event("shutdown")
    async def shutdown_event():
        logger.info("FastAPI Application shutting down.")
        
    return app

# Instantiated application block for seamless Uvicorn usage
app = create_app()

if __name__ == "__main__":
    import uvicorn
    logger.info("Starting local test server.")
    uvicorn.run(app, host="127.0.0.1", port=8000)
