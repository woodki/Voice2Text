class TranscriptionRepository:
    def __init__(self, connection):
        self.connection = connection

    def save(self, text: str, language: str, filename: str):
        cursor = self.connection.cursor()

        try:
            sql = """
                INSERT INTO transcriptions (text, language, filename)
                VALUES (%s, %s, %s)
            """
            cursor.execute(sql, (text, language, filename))
            self.connection.commit()

            return cursor.lastrowid

        except Exception:
            self.connection.rollback()
            raise

        finally:
            cursor.close()

    def get_all(self):
        cursor = self.connection.cursor()

        try:
            sql = """
                SELECT id, text, language, filename
                FROM transcriptions
                ORDER BY id DESC
            """
            cursor.execute(sql)
            return cursor.fetchall()

        finally:
            cursor.close()