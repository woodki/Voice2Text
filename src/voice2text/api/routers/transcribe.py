import logging
import os

from fastapi import APIRouter, UploadFile, File, HTTPException, Form, Depends
from pydantic import BaseModel
from typing import Literal
import tempfile
import shutil

from voice2text.api.dependencies import (
    get_voice2text_service,
    get_transcription_repository,
)
from voice2text.application.service import Voice2TextService
from voice2text.exceptions.errors import AudioProcessingError
from voice2text.database.transcription_repository import TranscriptionRepository

logger = logging.getLogger(__name__)

router = APIRouter()

class TranscribeResponse(BaseModel):
    text: str
@router.post(
    "/transcribe",
    response_model=TranscribeResponse
)

def transcribe_endpoint(
    audio: UploadFile = File(...),
    language_mode: Literal[
            "自动检测",
            "中文",
            "English"
    ] = Form("自动检测"),
    service: Voice2TextService = Depends(get_voice2text_service),
    repository: TranscriptionRepository = Depends(get_transcription_repository),
):
    if audio.content_type not in ["audio/wav", "audio/x-wav"]:
        raise HTTPException(
            status_code=400,
            detail="Unsupported audio file type"
        )

    with tempfile.NamedTemporaryFile(
            delete=False,
            suffix=".wav"
    ) as temp_file:
        shutil.copyfileobj(audio.file, temp_file)
        audio_path = temp_file.name
        print("临时文件路径：", audio_path)

    try:
        transcribed_text, language = service.transcribe(
            audio_path,
            language_mode
        )

        repository.save(
            transcribed_text,
            language,
            audio.filename
        )

    except AudioProcessingError:
        raise

    except Exception:
        logger.exception(
            "Unexpected error during transcription"
        )
        raise HTTPException(
            status_code=500,
            detail="Internal server error"
        )

    finally:
        if os.path.exists(audio_path):
            os.remove(audio_path)
            print("临时文件已删除：", audio_path)

    return TranscribeResponse(
        text=transcribed_text
    )