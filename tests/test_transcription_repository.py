import os

import mysql.connector
import pytest
from dotenv import load_dotenv

from voice2text.database.transcription_repository import TranscriptionRepository

load_dotenv()

@pytest.fixture
def db_connection():
    connection = mysql.connector.connect(
        host=os.getenv("DB_HOST"),
        port=int(os.getenv("DB_PORT", "3306")),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        database=os.getenv("DB_NAME"),
    )

    try:
        yield connection
    finally:
        connection.close()



def test_save(db_connection):
    repository = TranscriptionRepository(db_connection)

    record_id = repository.save(
        "Repository test",
        "English",
        "repository_test.wav"
    )

    try:
        cursor = db_connection.cursor()

        try:
            cursor.execute(
                """
                SELECT id, text, language, filename
                FROM transcriptions
                WHERE id = %s
                """,
                (record_id,)
            )

            record = cursor.fetchone()

            assert record is not None
            assert record[1:] == (
                "Repository test",
                "English",
                "repository_test.wav"
            )

        finally:
            cursor.close()

    finally:
        cursor = db_connection.cursor()

        try:
            cursor.execute(
                """
                DELETE FROM transcriptions
                WHERE id = %s
                """,
                (record_id,)
            )
            db_connection.commit()

        finally:
            cursor.close()


def test_get_all(db_connection):
    repository = TranscriptionRepository(db_connection)

    record_id = repository.save(
        "History test",
        "English",
        "history_test.wav"
    )

    try:
        records = repository.get_all()

        ids = [record[0] for record in records]
        assert ids == sorted(ids, reverse=True)

        assert any(
            record[0] == record_id
            and record[1:] == (
                "History test",
                "English",
                "history_test.wav"
            )
            for record in records
        )

    finally:
        cursor = db_connection.cursor()

        try:
            cursor.execute(
                "DELETE FROM transcriptions WHERE id = %s",
                (record_id,)
            )
            db_connection.commit()
        finally:
            cursor.close()
