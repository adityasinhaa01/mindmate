from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.routes import wellness, chat
from app.services.stress_engine import get_stress_engine


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Initialize and cache model artifacts during application startup
    try:
        engine = get_stress_engine()
        app.state.ml_ready = engine.is_loaded
    except Exception as e:
        app.state.ml_ready = False
        app.state.ml_error = str(e)
    yield


app = FastAPI(
    title="MindMate AI Service",
    version="1.0.0",
    description="Microservice for stress calculation, recommendations and Qwen AI Companion",
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(wellness.router)
app.include_router(chat.router)


@app.get("/health")
def health_check():
    try:
        engine = get_stress_engine()
        ml_ready = engine.is_loaded
    except Exception:
        ml_ready = False

    return {
        "status": "healthy",
        "provider": settings.AI_PROVIDER,
        "model": settings.AI_MODEL,
        "ml_model_loaded": ml_ready,
    }