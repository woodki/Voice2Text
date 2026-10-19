from fastapi.testclient import TestClient
from voice2text.api.main import app
from voice2text.api.dependencies import (
    get_voice2text_service,
    get_transcription_repository,
)
import pytest
from voice2text.exceptions.errors import AudioProcessingError

client = TestClient(app)

class FakeService:
    def transcribe(self, audio_path, language_mode):
        return "Hello world", "English"

class FakeErrorService:
    def transcribe(self, audio_path, language_mode):
        raise AudioProcessingError("Transcription failed")

class FakeTranscriptionRepository:
    def __init__(self):
        self.saved_records = []

    def save(self, text, language, filename):
        self.saved_records.append((text, language, filename))

class FakeFailingRepository:
    def save(self, text, language, filename):
        raise RuntimeError("Database save failed")

def override_get_voice2text_service():
    return FakeService()

def override_get_repository():
    return FakeTranscriptionRepository()

def override_get_error_service():
    return FakeErrorService()


@pytest.fixture
def fake_service_override():
    fake_repository = FakeTranscriptionRepository()

    app.dependency_overrides[
        get_voice2text_service
    ] = override_get_voice2text_service

    app.dependency_overrides[
        get_transcription_repository
    ] = lambda: fake_repository

    yield fake_repository

    app.dependency_overrides.pop(
        get_voice2text_service,
        None
    )

    app.dependency_overrides.pop(
        get_transcription_repository,
        None
    )

@pytest.fixture
def fake_error_service_override():
    app.dependency_overrides[
        get_voice2text_service
    ] = override_get_error_service

    app.dependency_overrides[
        get_transcription_repository
    ] = override_get_repository

    yield

    app.dependency_overrides.pop(
        get_voice2text_service,
        None
    )
    app.dependency_overrides.pop(
        get_transcription_repository,
        None
    )

def test_transcribe_success(fake_service_override):
    fake_repository = fake_service_override

    response = client.post(
        "/transcribe",
        files={
            "audio": (
                "test.wav",
                b"fake audio data",
                "audio/wav"
            )
        },
        data={
            "language_mode": "English"
        }
    )

    assert response.status_code == 200
    assert response.json() == {
        "text": "Hello world",
        "saved": True
    }
    assert fake_repository.saved_records == [
        ("Hello world", "English", "test.wav")
    ]

def test_transcribe_save_failure():
    app.dependency_overrides[
        get_voice2text_service
    ] = override_get_voice2text_service

    app.dependency_overrides[
        get_transcription_repository
    ] = lambda: FakeFailingRepository()

    try:
        response = client.post(
            "/transcribe",
            files={
                "audio": (
                    "test.wav",
                    b"fake audio data",
                    "audio/wav"
                )
            },
            data={
                "language_mode": "English"
            }
        )

        assert response.status_code == 200
        assert response.json() == {
            "text": "Hello world",
            "saved": False
        }

    finally:
        app.dependency_overrides.pop(
            get_voice2text_service,
            None
        )
        app.dependency_overrides.pop(
            get_transcription_repository,
            None
        )

def test_transcribe_invalid_file_type(fake_service_override):
    response = client.post(
        "/transcribe",
        files={
            "audio": (
                "test.mp3",
                b"fake audio data",
                "audio/mpeg"
            )
        }
    )

    assert response.status_code == 400
    assert response.json() == {
        "detail": "Unsupported audio file type"
    }

def test_transcribe_missing_file(fake_service_override):
    response = client.post("/transcribe")

    assert response.status_code == 422

def test_transcribe_service_error(fake_error_service_override):
    response = client.post(
        "/transcribe",
        files={
            "audio": (
                "test.wav",
                b"fake audio data",
                "audio/wav"
            )
        }
    )

    assert response.status_code == 500