"""
Main entry point for the FastAPI application managing AI agents with LangGraph.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config.settings import Settings
from app.api.v1.routers import agent_router

# Initialize FastAPI app
app_settings = Settings()
app = FastAPI(
    title=app_settings.PROJECT_NAME,
    description=app_settings.PROJECT_DESCRIPTION,
    version=app_settings.PROJECT_VERSION,
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "*"
        # "https://diracmurairi.me",
        # "https://www.diracmurairi.me",
        # "https://irembo-llm-v2.vercel.app",
        # "https://irembo-llm-v2.vercel.app",  # Allow only this origin
    ],  # Adjust this to restrict origins, e.g., ["https://example.com"]
    allow_credentials=True,
    allow_methods=["*"],  # Adjust to restrict methods, e.g., ["GET", "POST"]
    allow_headers=[
        "*"
    ],  # Adjust to restrict headers, e.g., ["Content-Type", "Authorization"]
)

app.include_router(router=agent_router.router)


@app.get("/")
async def root() -> dict[str, str]:
    """
    Root endpoint that returns a success message.

    Returns:
        dict[str, str]: A dictionary with a success message.
    """
    return {"message": "Up and running!"}


@app.on_event("startup")
async def startup_event():
    """
    Startup event handler for initializing necessary components.
    """
    print("Starting up the application and initializing necessary components.")
    # Load any settings or configurations if needed


@app.on_event("shutdown")
async def shutdown_event():
    """
    Shutdown event handler for cleaning up resources.
    """
    print("Shutting down the application.")


@app.get("/health", tags=["Health Check"])
async def health_check():
    """
    Health check endpoint to verify if the application is running.
    """
    return {"status": "healthy"}


# If you have middleware or exception handling, add them here
