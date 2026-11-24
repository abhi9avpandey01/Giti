from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.config import settings
from app.routes import auth, repositories, chat, indexing

app = FastAPI(
    title="Giti API",
    description="AI-Powered GitHub Codebase Assistant Backend",
    version="1.0.0"
)

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include Routers
app.include_router(auth.router)
app.include_router(repositories.router)
app.include_router(chat.router)
app.include_router(indexing.router)


@app.get("/")
def health_check():
    return {
        "status": "healthy",
        "service": "Giti Backend",
        "version": "1.0.0"
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host=settings.HOST, port=settings.PORT, reload=True)
