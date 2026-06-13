async def test_register_creates_user(client):
    response = await client.post(
        "/auth/register",
        json={
            "email": "test@example.com",
            "password": "password123",
        },
    )

    assert response.status_code == 200


async def test_register_duplicate_email(client):
    data = {
        "email": "duplicate@example.com",
        "password": "password123",
    }

    response = await client.post(
        "/auth/register",
        json=data,
    )

    assert response.status_code == 200

    response = await client.post(
        "/auth/register",
        json=data,
    )

    assert response.status_code == 400
    assert response.json()["detail"] == "Email already registered"


async def test_login_returns_access_token(client):
    user_data = {
        "email": "login@example.com",
        "password": "password123",
    }

    await client.post(
        "/auth/register",
        json=user_data,
    )

    response = await client.post(
        "/auth/login",
        json=user_data,
    )

    assert response.status_code == 200
    assert response.json()["access_token"]
    assert response.json()["token_type"] == "bearer"


async def test_login_rejects_invalid_password(client):
    await client.post(
        "/auth/register",
        json={
            "email": "wrong-password@example.com",
            "password": "password123",
        },
    )

    response = await client.post(
        "/auth/login",
        json={
            "email": "wrong-password@example.com",
            "password": "wrong-password",
        },
    )

    assert response.status_code == 401
    assert response.json()["detail"] == "Invalid credentials"


async def test_me_returns_current_user(client):
    user_data = {
        "email": "me@example.com",
        "password": "password123",
    }

    register_response = await client.post(
        "/auth/register",
        json=user_data,
    )
    login_response = await client.post(
        "/auth/login",
        json=user_data,
    )

    response = await client.get(
        "/auth/me",
        headers={
            "Authorization": f"Bearer {login_response.json()['access_token']}",
        },
    )

    assert response.status_code == 200
    assert response.json() == register_response.json()


async def test_me_requires_authentication(client):
    response = await client.get("/auth/me")

    assert response.status_code == 401


async def test_me_rejects_invalid_token(client):
    response = await client.get(
        "/auth/me",
        headers={
            "Authorization": "Bearer invalid-token",
        },
    )

    assert response.status_code == 401
    assert response.json()["detail"] == "Invalid token"
