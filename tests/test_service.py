from unittest.mock import Mock, patch
from voice2text.application.service import Voice2TextService

def test_service():
    transcriber = Mock()
    writer = Mock()

    transcriber.transcribe.return_value = ("Hello world.", "en")
    writer.save_markdown.return_value = "output/test.md"

    with patch(
        "voice2text.application.service.GeminiClient"
    ) as MockGeminiClient, patch(
        "voice2text.application.service.EnglishCorrector"
    ) as MockEnglishCorrector:
        mock_client = MockGeminiClient.return_value
        mock_corrector = MockEnglishCorrector.return_value
        mock_corrector.correct.side_effect = Exception(
            "Gemini unavailable"
        )

        service = Voice2TextService(
            transcriber,
            writer
        )

        result = service.process(
            "test.wav",
            "English",
            True,
            "chosen-output",
            "fake-api-key"
        )

        MockGeminiClient.assert_called_once_with(
            "fake-api-key"
        )

        MockEnglishCorrector.assert_called_once_with(
            mock_client
        )

        mock_corrector.correct.assert_called_once_with(
            "Hello world."
        )

    assert result == (
        "Hello world.",
        None,
        "output/test.md",
        "Gemini unavailable"
    )

    transcriber.transcribe.assert_called_once_with(
        "test.wav",
        "English"
    )

    writer.save_markdown.assert_called_once_with(
        "test.wav",
        "Hello world.",
        "chosen-output"
    )




