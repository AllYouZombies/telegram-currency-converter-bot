from dotenv import load_dotenv

from utils.env import get_env


# Load environment variables from .env file
load_dotenv()


# Telegram bot settings

# Telegram bot token
BOT_TOKEN = get_env('BOT_TOKEN')


# Database settings

# Database engine
DATABASE_URL = get_env('DATABASE_URL', 'sqlite:///./db.sqlite3')

