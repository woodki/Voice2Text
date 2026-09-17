import logging
import sys
from pathlib import Path


BASE_DIR = (
    Path(sys.executable).resolve().parent
    if getattr(sys, 'frozen', False)
    else Path(__file__).resolve().parents[2]
)


def setup_logging():

    log_folder = BASE_DIR / "logs"

    log_folder.mkdir(
        exist_ok=True
    )

    log_file = log_folder / "voice2text.log"

    logging.basicConfig(
        level=logging.INFO,

        format=(
            "%(asctime)s "
            "%(levelname)s:"
            "%(name)s:"
            "%(message)s"
        ),

        handlers=[
            logging.FileHandler(
                log_file,
                encoding="utf-8"
            ),
            *([logging.StreamHandler()] if sys.stderr is not None else [])
        ],
         force = True
    )