from unittest.mock import Mock

from voice2text.english_correction.corrector import EnglishCorrector


def test_correct_english():
    fake_client = Mock()
    fake_client.generate.return_value = "I am learning English."

    corrector = EnglishCorrector(fake_client)

    result = corrector.correct("I learning English.")

    assert result == "I am learning English."

    fake_client.generate.assert_called_once()