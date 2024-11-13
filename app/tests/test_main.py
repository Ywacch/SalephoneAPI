import pytest
from jsonschema import validate, ValidationError
from starlette.testclient import TestClient

from app.main import app

#TODO: response schema in  test_phone_all() should be in every request-response test

@pytest.fixture(scope="module")
def app_client():
    with TestClient(app) as client:
        yield client


def test_phone_all(app_client):
    response_schema = {
        "type": "array",
        "items": {  # Each item in the array should be a dictionary that matches phone_schema
            "type": "object",
            "properties": {
                "phone_id": {"type": "string"},
                "phone_name": {"type": "string"},
                "brand": {"type": "string"},
                "series": {"type": "string"},
                "model": {"type": "string"},
                "storage_size": {"type": "string"}
            },
            "required": ["phone_id", "phone_name"],  # Only phone_id and phone_name are mandatory
            "additionalProperties": True  # Allows other fields beyond those listed in `properties`
        }
    }

    response1 = app_client.get("/phones/?detailed=true")
    response2 = app_client.get("/phones/?detailed=false")
    response3 = app_client.get("/phones/")

    assert response1.status_code == 200
    assert response2.status_code == 200
    assert response3.status_code == 200


    try:
        validate(response1.json(), response_schema)
        assert True, "response 1 matches schema"
    except ValidationError as e:
        assert False, f'response 1 does not match schema {e}'

    try:
        validate(response2.json(), response_schema)
        assert True, "response matches schema"
    except ValidationError as e:
        assert False, f'response does not match schema {e}'

    try:
        validate(response3.json(), response_schema)
        assert True, "response matches schema"
    except ValidationError as e:
        assert False, f'response does not match schema {e}'



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

    assert len(response.json()) > 1

def test_price_history_invalid_time(app_client):
    _id = 'e6f4adaf6a82d2048ed867bbcc035190'

    response = app_client.get(f"/phones/{_id}/price_history?timeframe=invalid")

    assert response.status_code == 400

    assert response.json() == {"detail": "timestamp 'invalid' is not a valid parameter"}


def test_phone_brands(app_client):
    pass


def test_phone_series(app_client):
    pass
