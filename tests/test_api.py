"""Flask API integration tests."""

import pytest

from app import create_app


@pytest.fixture
def client():
    app = create_app()
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client


def test_health(client):
    res = client.get("/health")
    assert res.status_code == 200
    assert res.get_json()["status"] == "ok"


def test_list_algorithms(client):
    res = client.get("/api/algorithms")
    data = res.get_json()
    assert data["success"] is True
    assert len(data["algorithms"]) == 6
    assert "limits" in data


def test_generate_valid(client):
    res = client.post("/generate", json={"size": 10, "array_type": "random"})
    data = res.get_json()
    assert res.status_code == 200
    assert data["success"] is True
    assert len(data["array"]) == 10


def test_generate_invalid_size(client):
    res = client.post("/generate", json={"size": 9999, "array_type": "random"})
    assert res.status_code == 400


def test_sort_valid(client):
    res = client.post("/sort", json={
        "algorithm": "Bubble Sort",
        "array": [3, 1, 2],
    })
    data = res.get_json()
    assert res.status_code == 200
    assert data["result"]["sorted_array"] == [1, 2, 3]


def test_sort_invalid_array(client):
    res = client.post("/sort", json={"algorithm": "Bubble Sort", "array": ["a", "b"]})
    assert res.status_code == 400


def test_benchmark(client):
    res = client.post("/benchmark", json={"array": [5, 3, 1, 4, 2]})
    data = res.get_json()
    assert res.status_code == 200
    assert len(data["benchmark"]["results"]) == 6
    assert all(r["verified"] for r in data["benchmark"]["results"])
