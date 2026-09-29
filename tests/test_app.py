import io

from app import create_app


def test_health_endpoint():
    client = create_app({"TESTING": True}).test_client()
    assert client.get("/health").get_json() == {"status": "nominal", "version": "2.0.0"}


def test_uploaded_text_search():
    client = create_app({"TESTING": True}).test_client()
    response = client.post("/api/search", data={"query": "Thor", "source": "upload",
        "file": (io.BytesIO(b"Thor transmission complete"), "mission.txt")})
    assert response.status_code == 200
    assert response.get_json()["occurrences"] == 1


def test_search_requires_query():
    client = create_app({"TESTING": True}).test_client()
    assert client.post("/api/search", data={"query": ""}).status_code == 400
