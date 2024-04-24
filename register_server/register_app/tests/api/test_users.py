import pytest
from random import randint
from httpx import AsyncClient

from register_app.main import app
from register_app.core.config import settings

rand_num = randint(1, 9999)

test_data = {
    "email": f"assert{rand_num}@example.com",
    "password": "1",
    "nickname": f"assert{rand_num}",
    "permission": "user"
}

base_url = f"http://localhost{settings.PREFIX_URL}"


@pytest.mark.asyncio
async def test_root():
    async with AsyncClient(app=app, base_url=f"{base_url}") as ac:
        response = await ac.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "This is register server!!"}


@pytest.mark.asyncio
async def test_users_without_header():
    """
    헤더 없이 post
    """
    async with AsyncClient(app=app, base_url=f"{base_url}/users") as ac:
        response = await ac.post("/", json=test_data)
    assert response.status_code == 401 or 409
    assert response.json() == {
        "detail": {
            "error": "Unauthorized user",
            "message": "You do not have permission"
        }
    } or {"detail": {
        "error": "User already exists",
        "message": "The user with the provided nickname or email already exists."
    }}


@pytest.mark.asyncio
async def test_users_with_header():
    """
    헤더 있이 post
    """
    async with AsyncClient(app=app, base_url=f"{base_url}/users", headers={'SUPERUSER-HEADER': settings.SUPERUSER_HEADER}) as ac:
        response = await ac.post("/", json=test_data)
        print(response.url)
    assert response.status_code == 201
    assert response.json() == {"message": "User Create Successful"}
