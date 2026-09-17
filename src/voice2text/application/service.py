import logging

from voice2text.ai.gemini_client import GeminiClient
from voice2text.english_correction.corrector import EnglishCorrector

logger = logging.getLogger(__name__)


class Voice2TextService:
    def __init__(self, transcriber, writer):
        self.transcriber = transcriber
        self.writer = writer

    def process(
            self,
            audio_path,
            language_mode,
            use_ai_correction,
            output_folder,
            api_key=None
    ):

        transcribed_text, language = self.transcriber.transcribe(
            audio_path,
            language_mode
        )


        md_path = self.writer.save_markdown(
            audio_path,
            transcribed_text,
            output_folder
        )

        corrected_text = None
        ai_error = None

        if use_ai_correction:
            try:
                if not api_key:
                    raise ValueError("请先提供 Gemini API key")

                client = GeminiClient(api_key)
                corrector = EnglishCorrector(client)

                corrected_text = corrector.correct(
                    transcribed_text
                )
            except Exception as e:
                ai_error = str(e)
                logger.error(
                    "AI 纠错失败",
                    exc_info=True
                )

        return transcribed_text, corrected_text, md_path, ai_error