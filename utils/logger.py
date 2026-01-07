import logging
import sys
from config.settings import settings

def setup_logger(name: str = "orolar"):
    """
    ตั้งค่า Logger ให้มี format ที่อ่านง่าย
    """
    logger = logging.getLogger(name)

    # ถ้าตั้งค่าไปแล้วไม่ต้องทำซ้ำ
    if logger.handlers:
        return logger

    logger.setLevel(logging.DEBUG if settings.DEBUG else logging.INFO)

    # Format: [TIME] [LEVEL] [LOGGER] Message
    formatter = logging.Formatter(
        fmt="[%(asctime)s] [%(levelname)s] [%(name)s] %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )

    # Stream Handler (Output to Console)
    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(formatter)
    logger.addHandler(handler)

    return logger

# Singleton Logger Instance
logger = setup_logger()
