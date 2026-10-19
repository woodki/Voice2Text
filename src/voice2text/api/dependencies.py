from functools import lru_cache
from voice2text.application.service import Voice2TextService
from voice2text.output.markdown_writer import MarkdownWriter
from voice2text.transcription.funasr_nano_transcriber import FunASRNanoTranscriber
import os
import mysql.connector
from dotenv import load_dotenv
from voice2text.database.transcription_repository import TranscriptionRepository

load_dotenv()

@lru_cache
def get_voice2text_service():
    transcriber = FunASRNanoTranscriber()
    writer = MarkdownWriter()

    service = Voice2TextService(
        transcriber,
        writer
    )

    return service

def get_transcription_repository():
    connection = mysql.connector.connect(
        host=os.getenv("DB_HOST"),
        port=int(os.getenv("DB_PORT", "3306")),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        database=os.getenv("DB_NAME"),
    )

    try:
        yield TranscriptionRepository(connection)
    finally:
        connection.close()

