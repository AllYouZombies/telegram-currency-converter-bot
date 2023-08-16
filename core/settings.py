from dotenv import load_dotenv

from utils.env import get_env


# Load environment variables from .env file
load_dotenv()


# General settings

# Timezone
TIME_ZONE = get_env('TIME_ZONE', 'UTC')


# Telegram bot settings

# Telegram bot token
BOT_TOKEN = get_env('BOT_TOKEN')


# Database settings

# Database engine
DATABASE_URL = get_env('DATABASE_URL', 'sqlite+aiosqlite:///db.sqlite3')


# Localizations settings

# Default language
DEFAULT_LANGUAGE = get_env('DEFAULT_LANGUAGE', 'ru')

# Supported languages
SUPPORTED_LANGS = ['en', 'ru']


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
