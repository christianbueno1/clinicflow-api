from contextlib import asynccontextmanager

from fastapi import Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from clinicflow_api.config import get_settings
from clinicflow_api.database import engine, get_session
from clinicflow_api.routers import appointments, doctors, patients, specialties

settings = get_settings()


@asynccontextmanager
async def lifespan(app: FastAPI):
    yield
    await engine.dispose()


app = FastAPI(
    title="ClinicFlow API",
    version="0.1.0",
    lifespan=lifespan,
)

app.include_router(specialties.router)
app.include_router(doctors.router)
app.include_router(patients.router)
app.include_router(appointments.router)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["X-Total-Count"],
)


@app.get("/health")
async def health():
    return {"status": "ok"}


@app.get("/health/db")
async def database_health(
    session: AsyncSession = Depends(get_session),
):
    result = await session.execute(text("SELECT 1"))
    value = result.scalar_one()

    return {
        "status": "ok",
        "database": "connected",
        "result": value,
    }
