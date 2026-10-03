from fastapi.testclient import TestClient

from app.config import settings
from app.main import app


client = TestClient(app)


def test_home_page():
    response = client.get("/")

    assert response.status_code == 200
    assert "ComicCraft" in response.text


def test_health():
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_generate_validation():
    response = client.post(
        "/generate-comic/json",
        json={
            "prompt": "",
            "character_name": "Ravi",
            "setting": "A small Indian town",
            "tone": "Inspirational",
            "art_style": "2D cartoon style",
        },
    )

    assert response.status_code == 422


def test_form_validation_shows_error_instead_of_crashing():
    response = client.post("/generate", data={"prompt": "hi"})

    assert response.status_code == 422
    assert "Please check your inputs" in response.text


def test_missing_api_key_returns_clear_error(monkeypatch):
    monkeypatch.setattr(settings, "GEMINI_API_KEY", "")

    response = client.post("/generate", data={"prompt": "A farmer saves a village"})

    assert response.status_code == 503
    assert "GEMINI_API_KEY" in response.text


def test_download_missing_file_returns_404():
    assert client.get("/download/does-not-exist.pdf").status_code == 404


def test_download_blocks_path_traversal():
    response = client.get("/download/..%5Cpyproject.toml")

    assert response.status_code == 404
