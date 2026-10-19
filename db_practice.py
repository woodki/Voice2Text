import os
import mysql.connector
from voice2text.database.transcription_repository import TranscriptionRepository
from dotenv import load_dotenv

load_dotenv()

connection = mysql.connector.connect(
    host=os.getenv("DB_HOST"),
    port=int(os.getenv("DB_PORT", "3306")),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),
    database=os.getenv("DB_NAME"),
)

print("MySQL 连接成功！")

try:
    repository = TranscriptionRepository(connection)
    repository.save("Saved by Repository", "English")
    print("Repository 保存成功！")
finally:
    connection.close()