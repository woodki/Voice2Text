
from fastapi import APIRouter, Depends

from voice2text.api.dependencies import get_transcription_repository
from voice2text.database.transcription_repository import TranscriptionRepository

router = APIRouter()


@router.get("/history")
def get_history(
    repository: TranscriptionRepository = Depends(get_transcription_repository),
):
    records = repository.get_all()

    return [
        {
            "id": record[0],
            "text": record[1],
            "language": record[2],
            "filename": record[3],
        }
        for record in records
    ]
