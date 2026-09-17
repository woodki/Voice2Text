from voice2text.output.markdown_writer import MarkdownWriter
from voice2text.logging_config import setup_logging
from voice2text.application.service import Voice2TextService
from voice2text.transcription.funasr_nano_transcriber import FunASRNanoTranscriber
from voice2text.gui import start_gui

def main():
    setup_logging()

    transcriber = FunASRNanoTranscriber()
    writer = MarkdownWriter()

    service = Voice2TextService(
        transcriber,
        writer
    )

    start_gui(service)

if __name__ == "__main__":
    main()