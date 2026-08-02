import os

from dotenv import load_dotenv

load_dotenv()

DATABASE_NAME = os.getenv("DATABASE_NAME")
SERVER_NAME = os.getenv("SERVER_NAME")
DEFAULT_EXPIRY_DAYS = int(os.getenv("DEFAULT_EXPIRY_DAYS", "30"))