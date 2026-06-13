from datetime import UTC, datetime, timedelta

from app.core.database import AsyncSessionLocal
from app.modules.analytics.models import AnalyticsEvent
from app.modules.urls.models import ShortURL
from sqlalchemy import select


async def auth_headers(client, email: str = "user@example.com") -> dict[str, str]:
    password = "password123"

    await client.post(
        "/auth/register",
        json={
            "email": email,
            "password": password,
        },
    )

    response = await client.post(
        "/auth/login",
        json={
            "email": email,
            "password": password,
        },
    )

    return {
        "Authorization": f"Bearer {response.json()['access_token']}",
    }


async def test_create_url_requires_authentication(client):
    response = await client.post(
        "/urls",
        json={
            "original_url": "https://example.com",
        },
    )

    assert response.status_code == 401


async def test_create_url(authenticated_client):
    response = await authenticated_client.post(
        "/urls",
        json={
            "original_url": "https://example.com/somewhere",
        },
    )

    assert response.status_code == 200
    assert response.json()["original_url"] == "https://example.com/somewhere"
    assert len(response.json()["short_code"]) == 6
    assert response.json()["click_count"] == 0


async def test_create_url_returns_existing_duplicate(authenticated_client):
    payload = {
        "original_url": "https://example.com/duplicate",
    }

    first_response = await authenticated_client.post(
        "/urls",
        json=payload,
    )
    second_response = await authenticated_client.post(
        "/urls",
        json=payload,
    )

    assert first_response.status_code == 200
    assert second_response.status_code == 200
    assert second_response.json()["id"] == first_response.json()["id"]
    assert second_response.json()["short_code"] == first_response.json()["short_code"]


async def test_list_urls_is_paginated(authenticated_client):
    for index in range(3):
        await authenticated_client.post(
            "/urls",
            json={
                "original_url": f"https://example.com/page-{index}",
            },
        )

    response = await authenticated_client.get(
        "/urls?page=1&page_size=2",
    )

    assert response.status_code == 200
    assert response.json()["total"] == 3
    assert response.json()["page"] == 1
    assert response.json()["page_size"] == 2
    assert len(response.json()["items"]) == 2


async def test_list_urls_returns_only_current_users_urls(client):
    first_user_headers = await auth_headers(client, "first@example.com")
    second_user_headers = await auth_headers(client, "second@example.com")

    await client.post(
        "/urls",
        json={
            "original_url": "https://example.com/first-user",
        },
        headers=first_user_headers,
    )
    await client.post(
        "/urls",
        json={
            "original_url": "https://example.com/second-user",
        },
        headers=second_user_headers,
    )

    response = await client.get(
        "/urls",
        headers=first_user_headers,
    )

    assert response.status_code == 200
    assert response.json()["total"] == 1
    assert response.json()["items"][0]["original_url"] == "https://example.com/first-user"


async def test_update_url_expiration(authenticated_client):
    create_response = await authenticated_client.post(
        "/urls",
        json={
            "original_url": "https://example.com/update",
        },
    )
    expires_at = (datetime.now(UTC) + timedelta(days=1)).isoformat()

    response = await authenticated_client.patch(
        f"/urls/{create_response.json()['id']}",
        json={
            "expires_at": expires_at,
        },
    )

    assert response.status_code == 200
    assert response.json()["expires_at"] is not None


async def test_update_url_rejects_past_expiration(authenticated_client):
    create_response = await authenticated_client.post(
        "/urls",
        json={
            "original_url": "https://example.com/past",
        },
    )
    expires_at = (datetime.now(UTC) - timedelta(days=1)).isoformat()

    response = await authenticated_client.patch(
        f"/urls/{create_response.json()['id']}",
        json={
            "expires_at": expires_at,
        },
    )

    assert response.status_code == 400
    assert response.json()["detail"] == "Expiration time must be in the future"


async def test_delete_url(authenticated_client):
    create_response = await authenticated_client.post(
        "/urls",
        json={
            "original_url": "https://example.com/delete",
        },
    )

    delete_response = await authenticated_client.delete(
        f"/urls/{create_response.json()['id']}",
    )
    list_response = await authenticated_client.get(
        "/urls",
    )

    assert delete_response.status_code == 204
    assert list_response.json()["total"] == 0


async def test_user_cannot_delete_another_users_url(client):
    owner_headers = await auth_headers(client, "owner@example.com")
    other_headers = await auth_headers(client, "other@example.com")
    create_response = await client.post(
        "/urls",
        json={
            "original_url": "https://example.com/private",
        },
        headers=owner_headers,
    )

    response = await client.delete(
        f"/urls/{create_response.json()['id']}",
        headers=other_headers,
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "URL not found"


async def test_redirect_records_click_and_analytics_event(authenticated_client):
    create_response = await authenticated_client.post(
        "/urls",
        json={
            "original_url": "https://example.com/redirect",
        },
    )

    response = await authenticated_client.get(
        f"/r/{create_response.json()['short_code']}",
        follow_redirects=False,
    )

    assert response.status_code == 307
    assert response.headers["location"] == "https://example.com/redirect"

    async with AsyncSessionLocal() as db:
        url = await db.get(ShortURL, create_response.json()["id"])
        events = await db.execute(select(AnalyticsEvent))

    assert url.click_count == 1
    assert len(events.scalars().all()) == 1


async def test_redirect_rejects_expired_url(authenticated_client):
    create_response = await authenticated_client.post(
        "/urls",
        json={
            "original_url": "https://example.com/expired",
        },
    )

    async with AsyncSessionLocal() as db:
        url = await db.get(ShortURL, create_response.json()["id"])
        url.expires_at = datetime.now(UTC) - timedelta(days=1)
        await db.commit()

    response = await authenticated_client.get(
        f"/r/{create_response.json()['short_code']}",
        follow_redirects=False,
    )

    assert response.status_code == 410
    assert response.json()["detail"] == "URL has expired"


async def test_create_url_rate_limit(authenticated_client):
    for index in range(5):
        response = await authenticated_client.post(
            "/urls",
            json={
                "original_url": f"https://example.com/rate-limit-{index}",
            },
        )
        assert response.status_code == 200

    response = await authenticated_client.post(
        "/urls",
        json={
            "original_url": "https://example.com/rate-limit-exceeded",
        },
    )

    assert response.status_code == 429
    assert response.json()["detail"] == "Rate limit exceeded. Please try again later."
    assert response.headers["Retry-After"]
