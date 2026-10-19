from fastapi.testclient import TestClient

from voice2text.api.main import app
from voice2text.api.dependencies import get_transcription_repository


client = TestClient(app)


class FakeTranscriptionRepository:
    def __init__(self, records):
        self.records = records

    def get_all(self):
        return self.records


def override_get_repository(records):
    def dependency():
        return FakeTranscriptionRepository(records)

    return dependency


def test_get_history_success():
    fake_records = [
        (2, "Second record", "English", "second.wav"),
        (1, "First record", "Chinese", "first.wav"),
    ]

    app.dependency_overrides[
        get_transcription_repository
    ] = override_get_repository(fake_records)

    try:
        response = client.get("/history")

        assert response.status_code == 200
        assert response.json() == [
            {
                "id": 2,
                "text": "Second record",
                "language": "English",
                "filename": "second.wav",
            },
            {
                "id": 1,
                "text": "First record",
                "language": "Chinese",
                "filename": "first.wav",
            },
        ]
    finally:
        app.dependency_overrides.pop(
            get_transcription_repository,
            None
        )


def test_get_history_empty():
    app.dependency_overrides[
        get_transcription_repository
    ] = override_get_repository([])

    try:
        response = client.get("/history")

        assert response.status_code == 200
        assert response.json() == []
    finally:
        app.dependency_overrides.pop(
            get_transcription_repository,
            None
        )