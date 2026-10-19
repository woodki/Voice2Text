from fastapi import FastAPI
from voice2text.api.routers.transcribe import router as transcribe_router
from voice2text.api.routers.history import router as history_router
from voice2text.exceptions.errors import AudioProcessingError
from fastapi.responses import JSONResponse
from voice2text.logging_config import setup_logging

setup_logging()

app = FastAPI()

@app.exception_handler(AudioProcessingError)
async def audio_processing_error_handler(
    request,
    exc
):
    return JSONResponse(
        status_code=500,
        content={
            "error": "AUDIO_PROCESSING_FAILED",
            "message": str(exc)
        }
    )

app.include_router(transcribe_router)
app.include_router(history_router)