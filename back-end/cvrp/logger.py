import logging
import logging.config
from dotenv import load_dotenv

load_dotenv()
import os
if not os.path.exists('./logs'):
    os.makedirs('./logs')

from loguru import logger

logging.config.fileConfig("logging.ini")
customLogger = logging.getLogger("custom")
print("SERVICE_ENVIRONMENT: ",os.getenv('SERVICE_ENVIRONMENT'))
if os.getenv("SERVICE_ENVIRONMENT") == "development":
    customLogger = logger