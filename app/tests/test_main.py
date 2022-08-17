import pytest
from starlette.testclient import TestClient

from app.main import app


@pytest.fixture(scope="module")
def app_client():
    with TestClient(app) as client:
        yield client


def test_phone_all(app_client):
    response1 = app_client.get("/phones/?detailed=true")
    response2 = app_client.get("/phones/?detailed=false")
    response3 = app_client.get("/phones/")

    assert response1.status_code == 200
    assert response2.status_code == 200
    assert response3.status_code == 200

    assert response1.json() == [
        {"phone_id": "e6f4adaf6a82d2048ed867bbcc035190", "brand": "Apple", "series": "x", "model": "iPhone", "phone_name": "Apple iPhone x 64GB", "storage_size":"64 GB"},
        {"phone_id":"468c6d0b1910206717edd573c114b7ef","brand":"Apple","series":"x","model":"iPhone","phone_name":"Apple iPhone x 256GB","storage_size":"256 GB"},
        {"phone_id":"deec77415dbf07b417d7f243b9ed6572","brand":"Apple","series":"8","model":"iPhone","phone_name":"Apple iphone 8 64GB","storage_size":"64 GB"},
        {"phone_id":"2e7aeea336ff71ad8633a38e4625e56e","brand":"Apple","series":"8","model":"iPhone","phone_name":"Apple iphone 8 128GB","storage_size":"128 GB"}]

    assert response2.json() == [
        {'phone_id': 'e6f4adaf6a82d2048ed867bbcc035190', 'phone_name': 'Apple iPhone x 64GB'},
        {'phone_id': '468c6d0b1910206717edd573c114b7ef', 'phone_name': 'Apple iPhone x 256GB'},
        {'phone_id': 'deec77415dbf07b417d7f243b9ed6572', 'phone_name': 'Apple iphone 8 64GB'},
        {'phone_id': '2e7aeea336ff71ad8633a38e4625e56e', 'phone_name': 'Apple iphone 8 128GB'}
    ]

    assert response3.json() == [
        {'phone_id': 'e6f4adaf6a82d2048ed867bbcc035190', 'phone_name': 'Apple iPhone x 64GB'},
        {'phone_id': '468c6d0b1910206717edd573c114b7ef', 'phone_name': 'Apple iPhone x 256GB'},
        {'phone_id': 'deec77415dbf07b417d7f243b9ed6572', 'phone_name': 'Apple iphone 8 64GB'},
        {'phone_id': '2e7aeea336ff71ad8633a38e4625e56e', 'phone_name': 'Apple iphone 8 128GB'}
    ]


def test_phone_id(app_client):
    _id = 'e6f4adaf6a82d2048ed867bbcc035190'
    response = app_client.get(f"/phones/{_id}")
    
    assert response.status_code == 200
    
    assert response.json() == {'phone_id': 'e6f4adaf6a82d2048ed867bbcc035190', 'phone_name': 'Apple iPhone x 64GB'}


def test_none_existent_phone(app_client):
    _id = 'e6f4adaf6a82d2048ed867bbccfakeid'

    response = app_client.get(f"/phones/{_id}")

    assert response.status_code == 404

    assert response.json() == {"detail": "Item not found"}


def test_price_history(app_client):
    _id = 'e6f4adaf6a82d2048ed867bbcc035190'

    response = app_client.get(f"/phones/{_id}/price_history?timeline=year")

    assert response.status_code == 200

    assert response.json() == [{"phone_name":"Apple iPhone x 64GB","datetime":"2020-01-01T06:00:00+00:00","sample_size":9,"average":267.9,"cheapest":179.2,"costliest":364.8},{"phone_name":"Apple iPhone x 64GB","datetime":"2022-01-01T06:00:00+00:00","sample_size":7,"average":316.3,"cheapest":294.4,"costliest":320.0}]


def test_price_history_invalid_time(app_client):
    _id = 'e6f4adaf6a82d2048ed867bbcc035190'

    response = app_client.get(f"/phones/{_id}/price_history?timeframe=invalid")

    assert response.status_code == 400

    assert response.json() == {"detail": "timestamp 'invalid' is not a valid parameter"}
