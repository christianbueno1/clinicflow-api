import asyncio
import itertools
import os
from datetime import UTC, datetime, timedelta
from pathlib import Path

import pytest
import pytest_asyncio
from dotenv import load_dotenv
from httpx import ASGITransport, AsyncClient
from sqlalchemy import text
from sqlalchemy.engine import make_url
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy.pool import NullPool

from clinicflow_api.database import get_session
from clinicflow_api.main import app
from clinicflow_api.models import Base
from clinicflow_api.validators import validar_cedula_ecuador

load_dotenv(Path(__file__).resolve().parent.parent / ".env.test")


def _test_url() -> str:
    url = os.environ.get("TEST_DATABASE_URL")
    if not url:
        raise RuntimeError(
            "Define TEST_DATABASE_URL en .env.test, por ejemplo: "
            "postgresql+psycopg://krs:PASSWORD@localhost:5432/clinicflow_test"
        )
    if not make_url(url).database.endswith("_test"):
        raise RuntimeError("TEST_DATABASE_URL debe apuntar a una base *_test")
    return url


TEST_URL = _test_url()

_counter = itertools.count(1)


def make_cedula(base9: str) -> str:
    total = 0
    for i, ch in enumerate(base9):
        d = int(ch) * (2 if i % 2 == 0 else 1)
        total += d - 9 if d > 9 else d
    cedula = base9 + str((10 - total % 10) % 10)
    assert validar_cedula_ecuador(cedula)
    return cedula


def future(days: int = 7, hour: int = 9, minute: int = 0) -> datetime:
    """Fecha futura en UTC, relativa a hoy, para que los tests no caduquen."""
    base = datetime.now(UTC) + timedelta(days=days)
    return base.replace(hour=hour, minute=minute, second=0, microsecond=0)


@pytest.fixture(scope="session", autouse=True)
def _schema():
    async def setup():
        engine = create_async_engine(TEST_URL, poolclass=NullPool)
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.drop_all)
            await conn.run_sync(Base.metadata.create_all)
        await engine.dispose()

    asyncio.run(setup())


@pytest_asyncio.fixture
async def client():
    engine = create_async_engine(TEST_URL, poolclass=NullPool)
    factory = async_sessionmaker(engine, expire_on_commit=False)

    async def override():
        async with factory() as session:
            yield session

    app.dependency_overrides[get_session] = override
    async with AsyncClient(
        transport=ASGITransport(app=app), base_url="http://test"
    ) as c:
        yield c
    app.dependency_overrides.clear()

    async with engine.begin() as conn:
        await conn.execute(
            text("TRUNCATE appointments, doctors, patients, specialties CASCADE")
        )
    await engine.dispose()


@pytest.fixture
def make_specialty(client):
    async def _make(name: str | None = None) -> dict:
        n = next(_counter)
        r = await client.post(
            "/specialties", json={"name": name or f"Especialidad {n}"}
        )
        assert r.status_code == 201, r.text
        return r.json()

    return _make


@pytest.fixture
def make_doctor(client, make_specialty):
    async def _make(last_name: str = "House", **overrides) -> dict:
        n = next(_counter)
        specialty_id = (
            overrides.pop("specialty_id", None) or (await make_specialty())["id"]
        )
        payload = {
            "first_name": "Gregory",
            "last_name": last_name,
            "identification_number": make_cedula(f"17{n:07d}"),
            "license_number": f"PPTH-{n:04d}",
            "specialty_id": specialty_id,
            **overrides,
        }
        r = await client.post("/doctors", json=payload)
        assert r.status_code == 201, r.text
        return r.json()

    return _make


@pytest.fixture
def make_patient(client):
    async def _make(last_name: str = "Warner", **overrides) -> dict:
        n = next(_counter)
        payload = {
            "first_name": "Stacy",
            "last_name": last_name,
            "date_of_birth": "1968-03-14",
            "sex": "female",
            "phone": "0991000001",
            "identification_number": make_cedula(f"18{n:07d}"),
            **overrides,
        }
        r = await client.post("/patients", json=payload)
        assert r.status_code == 201, r.text
        return r.json()

    return _make


@pytest.fixture
def book(client):
    async def _book(
        patient: dict, doctor: dict, starts_at: datetime, minutes: int = 30
    ):
        return await client.post(
            "/appointments",
            json={
                "patient_id": patient["id"],
                "doctor_id": doctor["id"],
                "starts_at": starts_at.isoformat(),
                "duration_minutes": minutes,
            },
        )

    return _book
