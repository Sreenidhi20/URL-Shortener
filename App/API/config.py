from dotenv import load_dotenv
import os

load_dotenv()

DATABASE_NAME = os.getenv("DATABASE_NAME")
SERVER_NAME = os.getenv("SERVER_NAME")