import pytest
from starlette.testclient import TestClient
from httpx import AsyncClient

from app.main import app


@pytest.fixture(scope="module")
def app_client():
    with TestClient(app) as client:
        yield client


@pytest.mark.skip
def test_phone_all(app_client):
    response = app_client.get("/phones/")

    assert response.status_code == 200

    assert response.json() == [
        {'phone_id': 'e6f4adaf6a82d2048ed867bbcc035190', 'phone_name': 'Apple iPhone x 64GB'},
        {'phone_id': '468c6d0b1910206717edd573c114b7ef', 'phone_name': 'Apple iPhone x 256GB'},
        {'phone_id': 'deec77415dbf07b417d7f243b9ed6572', 'phone_name': 'Apple iphone 8 64GB'},
        {'phone_id': '2e7aeea336ff71ad8633a38e4625e56e', 'phone_name': 'Apple iphone 8 128GB'}
    ]


@pytest.mark.skip
def test_phone_id(app_client):
    _id = 'e6f4adaf6a82d2048ed867bbcc035190'
    response = app_client.get(f"/phones/{_id}")
    
    assert response.status_code == 200
    
    assert response.json() == {'phone_id': 'e6f4adaf6a82d2048ed867bbcc035190', 'phone_name': 'Apple iPhone x 64GB'}


@pytest.mark.skip
def test_none_existent_phone(app_client):
    _id = 'e6f4adaf6a82d2048ed867bbccfakeid'

    response = app_client.get(f"/phones/{_id}")

    assert response.status_code == 404

    assert response.json() == {"detail": "Item not found"}

