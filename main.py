import asyncio
import logging

from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, Application, InlineQueryHandler, MessageHandler, filters, \
    Defaults

from bot import commands, inlines
from bot.menus.dispatcher import menu_dispatcher
from core.settings import BOT_TOKEN, persistence, SUPPORTED_LANGS
from utils.localization import activate_locale, rev_translate

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)

# set higher logging level for httpx to avoid all GET and POST requests being logged
logging.getLogger("httpx").setLevel(logging.WARNING)

logging = logging.getLogger(__name__)


async def _setup_commands(application: Application) -> None:
    """
    Set bot commands.
    This method is called after bot initialization. It imports all commands from bot/commands.py
    and sets them as bot commands.

    :param application: Application instance
    :type application: Application
    """

    logging.info("Deleting existing bot commands...")
    await application.bot.delete_my_commands()
    logging.info("Setting up bot commands...")
    for code, name in SUPPORTED_LANGS:
        activate_locale(code)
        available_commands = [cmd for cmd in dir(commands) if cmd.startswith('command_')]
        _commands = [(cmd[8:], _(rev_translate(getattr(commands, cmd).__doc__))) for cmd in available_commands]
        await application.bot.set_my_commands(
            language_code=code,
            commands=_commands
        )
    logging.info("Bot commands set up successfully.")


async def _setupcommand_handlers(application: Application) -> None:
    """
    Set up command handlers.
    This method adds command handlers for available commands.

    :param application: Application instance
    :type application: Application
    """

    logging.info("Setting up command handlers...")
    available_commands = [cmd for cmd in dir(commands) if cmd.startswith('command_')]

    async def __addcommand_handler(cmd):
        application.add_handler(CommandHandler(cmd[8:], getattr(commands, cmd)))

    await asyncio.gather(*[__addcommand_handler(cmd) for cmd in available_commands])
    logging.info("Command handlers set up successfully.")


async def _setup_menu_dispatcher(application: Application) -> None:
    """
    Set up dispatcher for menu buttons.
    Because menu buttons can be localized, we can't set separate handlers for each button.
    This method adds a single handler for all menu buttons.
    Dispatcher handles all menu buttons and calls corresponding menu handlers.

    :param application: Application instance
    """

    logging.info("Setting up menu dispatcher...")
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, menu_dispatcher))
    logging.info("Menu dispatcher set up successfully.")


async def _setup_inline_handlers(application: Application) -> None:
    """
    Set up inline handlers.
    This method adds inline query handlers for available inline commands.

    :param application: Application instance
    :type application: Application
    """

    logging.info("Setting up inline handlers...")
    available_inline_handlers = [cmd for cmd in dir(inlines) if cmd.startswith('_inline_')]

    async def __add_inline_handler(cmd):
        application.add_handler(InlineQueryHandler(getattr(inlines, cmd)))

    await asyncio.gather(*[__add_inline_handler(cmd) for cmd in available_inline_handlers])
    logging.info("Inline handlers set up successfully.")


async def post_init(application: Application) -> None:
    """
    Perform post-initialization tasks.
    This method initializes database models, deletes existing bot commands, and sets up command and inline query handlers.

    :param application: Application instance
    :type application: Application
    """

    logging.info("Performing post-initialization tasks...")
    await _setup_commands(application)
    await _setupcommand_handlers(application)
    await _setup_inline_handlers(application)
    await _setup_menu_dispatcher(application)
    logging.info("Post-initialization tasks completed.")


def main():
    """
    Main entry point for the Telegram bot application.
    """

    logging.info("Starting the Telegram bot application...")
    defaults = Defaults(parse_mode='HTML')
    app_instance = ApplicationBuilder().token(BOT_TOKEN) \
        .persistence(persistence) \
        .defaults(defaults) \
        .post_init(post_init) \
        .build()

    app_instance.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == '__main__':
    main()
