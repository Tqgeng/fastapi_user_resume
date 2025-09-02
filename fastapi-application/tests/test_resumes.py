import pytest
from httpx import (
    AsyncClient,
    ASGITransport,
)
import pytest_asyncio

from core.models import db_helper
from main import main_app
from .config import (
    auth_register,
    auth_login,
    resume,
    resume_for_id,
)

pytestmark = pytest.mark.asyncio


@pytest_asyncio.fixture
async def client():
    transport = ASGITransport(app=main_app)
    async with AsyncClient(transport=transport, base_url="http://test") as ac:
        yield ac


@pytest_asyncio.fixture(autouse=True)
async def up_db():
    yield
    await db_helper.dispose()


@pytest_asyncio.fixture
async def auth_headers(client):
    register_data = {
        "email": "testuser@example.com",
        "password": "123",
    }
    await client.post(auth_register(), json=register_data)

    login_data = {
        "username": register_data["email"],
        "password": register_data["password"],
    }
    response = await client.post(auth_login(), data=login_data)
    assert response.status_code == 200
    token = response.json()["access_token"]

    return {"Authorization": f"Bearer {token}"}


async def test_create_resume(client, auth_headers):
    response = await client.post(
        resume(),
        headers=auth_headers,
        json={"title": "Python Backend Dev", "content": "FastAPI, SQLAlchemy"},
    )
    assert response.status_code in (200, 201)
    data = response.json()
    assert data["title"] == "Python Backend Dev"
    assert "id" in data


async def test_get_resumes(client, auth_headers):
    await client.post(
        resume(),
        headers=auth_headers,
        json={"title": "Golang Dev", "content": "Microservices"},
    )

    response = await client.get(resume(), headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) >= 1


async def test_get_resume_by_id(client, auth_headers):
    create = await client.post(
        resume(),
        headers=auth_headers,
        json={"title": "Data Engineer", "content": "ETL, Airflow"},
    )
    resume_id = create.json()["id"]

    response = await client.get(resume_for_id(resume_id), headers=auth_headers)
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == resume_id
    assert data["title"] == "Data Engineer"


async def test_update_resume(client, auth_headers):
    create = await client.post(
        resume(),
        headers=auth_headers,
        json={"title": "Junior QA", "content": "Manual"},
    )
    resume_id = create.json()["id"]

    response = await client.patch(
        resume_for_id(resume_id),
        headers=auth_headers,
        json={"title": "Middle QA", "content": "Automation"},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Middle QA"
    assert data.get("content") in (
        "Automation",
        None,
    )


async def test_delete_resume(client, auth_headers):
    create = await client.post(
        resume(),
        headers=auth_headers,
        json={"title": "ML Engineer", "content": "PyTorch"},
    )
    resume_id = create.json()["id"]

    response = await client.delete(resume_for_id(resume_id), headers=auth_headers)
    assert response.status_code == 200

    response = await client.get(resume_for_id(resume_id), headers=auth_headers)
    assert response.status_code == 404
