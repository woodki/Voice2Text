import pytest

from voice2text.text_processing import convert_punctuation


@pytest.mark.parametrize(
    "input_text, expected",
    [
        ("你好,世界", "你好，世界"),
        ("你好.世界", "你好。世界"),
        ("你好,世界?", "你好，世界？"),
        ("你好,世界!", "你好，世界！"),
        ("", ""),
        ("你好世界", "你好世界"),
        ("你好，世界。", "你好，世界。"),
    ]
)
def test_convert_punctuation(input_text, expected):
    result = convert_punctuation(input_text)
    assert result == expected