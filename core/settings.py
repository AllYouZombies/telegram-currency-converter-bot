import gettext
from pathlib import Path

from dotenv import load_dotenv
from telegram.ext import PicklePersistence

from utils.env import get_env

# Activate gettext to get translations working. See:
# https://docs.python.org/3/library/gettext.html
# It is important to initialize gettext before importing any other modules.
# Otherwise, translations won't work. Or even worse, you'll get an error saying
# that _() is not defined.
gettext.translation('messages', localedir='locale', languages=['en']).install(names=['_'])

# Load environment variables from .env file
load_dotenv()


# General settings

BASE_DIR = Path(__file__).resolve().parent.parent

BASE_CURR = "UZS"

SUPPORTED_CURRENCIES = [
    "USD",
    "RUB",
    "KZT",
    "EUR",
]

GETGEOAPI_KEY = get_env('GETGEOAPI_KEY')
GETGEOAPI_DAILY_REQUESTS_LIMIT = 48
GETGEOAPI_UPDATE_INTERVAL = int((60 * 60 * 60 * 24 / (GETGEOAPI_DAILY_REQUESTS_LIMIT / len(SUPPORTED_CURRENCIES))) / 2)

UZUM_BANK_UPDATE_INTERVAL = 60 * 60

PULTOP_SCRAPE_INTERVAL = 30

# Timezone
TIME_ZONE = get_env('TIME_ZONE', 'UTC')


# Telegram bot settings

# Telegram bot token
BOT_TOKEN = get_env('BOT_TOKEN')

# Peristence settings
PERSISTENCE_CLASS = PicklePersistence
persistence = PERSISTENCE_CLASS(BASE_DIR / 'persistence.pickle')


# Database settings

# Database engine
if DB_HOST := get_env('DB_HOST'):
    DB_PORT = get_env('DB_PORT')
    DB_NAME = get_env('DB_NAME')
    DB_USER = get_env('DB_USER')
    DB_PASSWORD = get_env('DB_PASSWORD')
    DATABASE_URL = f'postgresql+asyncpg://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}'
else:
    DATABASE_URL = get_env('DATABASE_URL', 'sqlite+aiosqlite:///db.sqlite3')


# Localizations settings

# Default language
DEFAULT_LANGUAGE = get_env('DEFAULT_LANGUAGE', 'ru')

# Supported languages
SUPPORTED_LANGS = (
    ('ru', _('Russian')),
    ('en', _('English')),
)

# Locale directory
LOCALE_DIR = BASE_DIR / 'locale'


# Redis settings

# Get Redis base URL
REDIS_BASE_URL = get_env('REDIS_BASE_URL', 'redis://localhost:6379')


# Celery settings
# https://docs.celeryproject.org/en/stable/userguide/configuration.html#new-lowercase-settings

# Broker URL
CELERY_BROKER_URL = REDIS_BASE_URL + '/0'
# Enable UTC
CELERY_ENABLE_UTC = True
# Task default queue
CELERY_TASK_DEFAULT_QUEUE = 'default'

