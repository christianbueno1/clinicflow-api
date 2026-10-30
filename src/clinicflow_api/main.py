from contextlib import asynccontextmanager

from fastapi import Depends, FastAPI
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from clinicflow_api.database import engine, get_session


@asynccontextmanager
async def lifespan(app: FastAPI):
    yield
    await engine.dispose()


app = FastAPI(
    title="ClinicFlow API",
    version="0.1.0",
    lifespan=lifespan,
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
