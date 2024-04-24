import pytest
from httpx import AsyncClient

from auth_app.main import app
from auth_app.core.config import settings

origin_user = {
    "email": "superuser@example.com",
    "password": "1"
}

wrong_email_user = {
    "email": "wrong@example.com",
    "password": "1"
}

wrong_password_user = {
    "email": "superuser@example.com",
    "password": "123"
}

base_url = f"http://localhost{settings.PREFIX_URL}"


@pytest.mark.asyncio
async def test_root():
    async with AsyncClient(app=app, base_url=f"{base_url}") as ac:
        response = await ac.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "This is auth server!!"}


@pytest.mark.asyncio
async def test_check_without_token():
    """
    토큰 없이 토큰을 확인
    """
    async with AsyncClient(app=app, base_url=f"{base_url}") as ac:
        response = await ac.get("/login/check")
    assert response.status_code == 400
    assert response.json() == {
        "detail": "Access token not found in cookie"
    }


@pytest.mark.asyncio
async def test_wrong_login():
    """
    1. 없는 사용자가
    2. 패스워드가 틀렸을때
    """
    assert_response = {
        "detail": {
            "error": "Not Found",
            "message": "The user does not exist on this system or the password is incorrect."
        }
    }

    async with AsyncClient(app=app, base_url=f"{base_url}") as ac:
        # case 1 없는 사용자 로그인
        response = await ac.post("/login/access-token", json=wrong_email_user)
        assert response.status_code == 400
        assert response.json() == assert_response

        # case 2 비밀번호가 틀린 로그인
        response = await ac.post("/login/access-token", json=wrong_password_user)
        assert response.status_code == 400
        assert response.json() == assert_response


@pytest.mark.asyncio
async def test_with_fake_token():
    """
    1.로그인 성공 후
    2.토큰을 변조
    3.토큰을 확인
    """
    sccuess_login_response = {
        "message": "Sucess Login User"
    }

    fail_check_response = {
        "detail": "Could not validate credentials"
    }

    async with AsyncClient(app=app, base_url=f"{base_url}") as ac:
        # 1. 로그인 성공
        response = await ac.post("/login/access-token", json=origin_user)
        assert response.status_code == 200
        assert response.json() == sccuess_login_response
        # 2. 토큰의 payload 변조
        # payload 중 만료일(exp값를 2027년까지로 변경)
        origin_header, _, origin_signatuer = response.cookies['access_token'].split(
            '.')
        fake_payload = "eyJlbWFpbCI6InN1cGVydXNlckBleGFtcGxlLmNvbSIsIm5pY2tuYW1lIjoic3VwZXJ1c2VyIiwicGVybWlzc2lvbiI6InN1cGVydXNlciIsImV4cCI6MTgxMzQ0OTQzMX0"
        fake_jwt = origin_header + '.' + fake_payload + '.' + origin_signatuer
        # 3. 변조한 토큰으로 확인요청
        response = await ac.get("/login/check", cookies={'access_token': fake_jwt})
        assert response.status_code == 401
        assert response.json() == fail_check_response


@pytest.mark.asyncio
async def test_with_sccuess_token():
    """
    1.로그인 성공 후
    2.토큰을 확인
    """
    sccuess_login_response = {
        "message": "Sucess Login User"
    }

    success_check_response = {
        "message": "Sucess Validate Token"
    }

    async with AsyncClient(app=app, base_url=f"{base_url}") as ac:
        # 1. 로그인 성공
        response = await ac.post("/login/access-token", json=origin_user)
        assert response.status_code == 200
        assert response.json() == sccuess_login_response
        # 2. 정상 토큰으로 확인요청
        response = await ac.get("/login/check", cookies={'access_token': response.cookies['access_token']})
        assert response.status_code == 200
        assert response.json() == success_check_response
