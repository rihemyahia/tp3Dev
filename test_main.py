
from fastapi.testclient import TestClient
from main import app, home

client = TestClient(app)


def test_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "it works!"}


def test_home():
    assert home() == {"message": "it works!"}


def test_addition():
    response = client.get("/addition?a=10&b=5")
    assert response.status_code == 200
    assert response.json() == {"result": 15.0}


def test_soustraction():
    response = client.get("/soustraction?a=10&b=5")
    assert response.status_code == 200
    assert response.json() == {"result": 5.0}


def test_greeting():
    response = client.get("/greeting?name=Rihem")
    assert response.status_code == 200
    data = response.json()

    assert data["message"] == "Hello, Rihem"
    assert data["developer"] == "Dev2"
    assert "hostname" in data
    assert "IP" in data


def test_multiply():
    response = client.post("/multiply", json={"a": 4, "b": 5})
    assert response.status_code == 200
    assert response.json() == {
        "result": 20.0,
        "developper": "Dev1"
    }


def test_divide():
    response = client.post("/divide", json={"a": 10, "b": 2})
    assert response.status_code == 200
    assert response.json() == {"result": 5.0}


def test_divide_by_zero():
    response = client.post("/divide", json={"a": 10, "b": 0})
    assert response.status_code == 400
    assert response.json() == {
        "detail": "Division by zero is not allowed"
    }


def test_remove():
    response = client.delete("/remove/5")
    assert response.status_code == 200
    assert response.json() == {"message": "Item 5 removed"}


def test_update():
    response = client.put(
        "/update/1",
        json={"name": "updated_item", "value": 50}
    )

    assert response.status_code == 200
    assert response.json() == {
        "id": 1,
        "item": {"name": "updated_item", "value": 50.0}
    }


def test_update_not_found():
    response = client.put(
        "/update/999",
        json={"name": "unknown", "value": 10}
    )

    assert response.status_code == 404
    assert response.json() == {"detail": "Item not found"}
