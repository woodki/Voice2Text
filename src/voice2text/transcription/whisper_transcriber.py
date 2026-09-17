import whisper
import logging

logger = logging.getLogger(__name__)

WHISPER_MODEL = "medium"

class WhisperTranscriber:
    def __init__(self):
        self.model = None

    def transcribe(self, audio_path, language_mode="自动检测"):
        if self.model is None:
            self.model = whisper.load_model(WHISPER_MODEL)

        # 根据用户选择决定语言
        if language_mode == "中文":
            language = "zh"
        elif language_mode == "English":
            language = "en"
        else:
            language = self.detect_audio_language(audio_path)

        logger.info(
            f"检测语言: {language}"
        )

        # 根据语言设置转写参数
        if language == "zh":
            result = self.model.transcribe(
                audio_path,
                language="zh",
                initial_prompt=(
                    "这是普通话录音的文字稿。"
                    "今天天气很好，我准备出去走走。"
                    "你今天怎么样？希望一切顺利！"
                )
            )
        else:
            result = self.model.transcribe(
                audio_path,
                language=language
            )

        text = result["text"]

        logger.info("Whisper转换完成")

        return text, language

    def detect_audio_language(self, audio_path):
        """检测音频语言。"""

        # 跳过前 10 秒后取一段用于语言检测
        audio = whisper.load_audio(audio_path)

        # 跳过开头 10 秒
        audio = audio[10 * 16000:]

        # 截取 30 秒用于语言检测
        audio = whisper.pad_or_trim(audio)

        # 转换成 Whisper 使用的频谱
        mel = whisper.log_mel_spectrogram(
            audio,
            n_mels=self.model.dims.n_mels
        ).to(self.model.device)

        # 获取各语言概率
        _, probabilities = self.model.detect_language(mel)

        # 打印中英文概率
        print("English:", probabilities.get("en", 0))
        print("Chinese:", probabilities.get("zh", 0))

        # 选择概率最高的语言
        language = max(probabilities, key=probabilities.get)

        return language