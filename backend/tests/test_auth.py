async def test_register(client):
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
