import logging
from pathlib import Path

LOGGING_FORMAT = "%(asctime)s - %(levelname)s - %(message)s"
LOG_DATA_FORMAT = "%d.%m.%y %H:%M:%S"
LOG_LVL = logging.INFO

PROJECT_DIR = Path(__file__).parent.parent.resolve()
SAVE_DIR = PROJECT_DIR / "processed"
