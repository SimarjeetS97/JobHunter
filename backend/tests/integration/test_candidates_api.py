import pytest

from backend.tests.utils.assertions import assert_error_shape, assert_validation_error


@pytest.mark.anyio
async def test_create_candidate_success(async_client):
    payload = {"email": "new.user@example.com", "name": "New User", "years_experience": 4}
    response = await async_client.post("/api/candidates", json=payload)

    # Accept either 200 or 201 to keep this portable while still asserting success contract.
    assert response.status_code in {200, 201}
    body = response.json()
    assert body.get("email") == payload["email"]


@pytest.mark.anyio
async def test_create_candidate_validation_error(async_client):
    payload = {"email": "not-an-email", "name": "A", "years_experience": -3}
    response = await async_client.post("/api/candidates", json=payload)

    assert response.status_code == 422
    body = response.json()
    assert_validation_error(body, field="email")


@pytest.mark.anyio
async def test_not_found_error_shape(async_client):
    response = await async_client.get("/api/candidates/99999999")
    assert response.status_code in {404, 422}
    assert_error_shape(response.json())
