from funasr import AutoModel
import logging

logger = logging.getLogger(__name__)


class FunASRNanoTranscriber:
    def __init__(self):
        self.model = None

    def transcribe(self, audio_path, language_mode="自动检测"):
        if self.model is None:
            self.model = AutoModel(
                model="FunAudioLLM/Fun-ASR-Nano-2512",
                vad_model="fsmn-vad",
                vad_kwargs={"max_single_segment_time": 30000},
                device="cuda:0",
            )

        if language_mode == "中文":
            model_language = "中文"
            language = "zh"
        elif language_mode == "English":
            model_language = "英文"
            language = "en"
        else:
            model_language = None
            language = None

        if model_language is None:
            result = self.model.generate(
                input=audio_path
            )
        else:
            result = self.model.generate(
                input=audio_path,
                language=model_language
            )

        text = result[0]["text"]

        logger.info("FunASRNano转换完成")

        return text, language