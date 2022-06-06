import logging
from os import getenv

from dotenv import load_dotenv
from pymongo import MongoClient

load_dotenv()

logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)

API_KEY = getenv("API_KEY")
API_HASH = getenv("API_HASH")
TOKEN = getenv("TOKEN")
DB_URL = getenv("DB_URL")
IMDB_API = getenv("IMDB_API")
PORT = int(getenv("PORT", 80))

# bot = TelegramClient(None, API_KEY, API_HASH)

if DB_URL:
    DB = MongoClient(DB_URL)
else:
    DB = None
