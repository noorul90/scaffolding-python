import pytest
from httpx import AsyncClient
from app.core.config import settings

@pytest.mark.asyncio
async def test_create_user_success(client: AsyncClient):
    payload = {
        "email": "testuser@example.com",
        "password": "supersecurepassword123"
    }
    
    response = await client.post(
        f"{settings.API_V1_STR}/users/", 
        json=payload
    )
    
    assert response.status_code == 201
    data = response.json()
    assert data["email"] == payload["email"]
    assert "id" in data
    assert data["is_active"] is True

@pytest.mark.asyncio
async def test_create_user_duplicate_email(client: AsyncClient):
    payload = {
        "email": "duplicate@example.com",
        "password": "supersecurepassword123"
    }
    
    # First creation call should pass smoothly
    first_res = await client.post(f"{settings.API_V1_STR}/users/", json=payload)
    assert first_res.status_code == 201
    
    # Second duplicate creation call must register a bad request failure
    second_res = await client.post(f"{settings.API_V1_STR}/users/", json=payload)
    assert second_res.status_code == 400
    assert second_res.json()["detail"] == "Email already registered."
