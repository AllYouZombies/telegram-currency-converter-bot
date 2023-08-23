import asyncio
import logging
import os

from telegram.ext import ApplicationBuilder, CommandHandler, Application, InlineQueryHandler

from core.db import engine, Base
from core.settings import BOT_TOKEN, persistence, SUPPORTED_LANGS, BASE_DIR
from utils.localization import activate_locale, rev_translate
from bot import commands, inlines


for lib in ['httpx', 'telegram', 'httpcore']:
    lib_logger = logging.getLogger(lib)
    lib_logger.setLevel(logging.WARNING)

log = logging.getLogger('core')
logging.basicConfig(level=logging.DEBUG)


async def _setup_commands(application: Application) -> None:
    """
    Set bot commands.
    This method is called after bot initialization. It imports all commands from bot/commands.py
    and sets them as bot commands.

    :param application: Application instance
    :type application: Application
    """

    log.info("Setting up bot commands...")
    for lang in SUPPORTED_LANGS:
        activate_locale(lang)
        available_commands = [cmd for cmd in dir(commands) if cmd.startswith('_command_')]
        _commands = [(cmd[9:], _(rev_translate(getattr(commands, cmd).__doc__))) for cmd in available_commands]
        await application.bot.set_my_commands(
            language_code=lang,
            commands=_commands
        )
    log.info("Bot commands set up successfully.")


async def _setup_command_handlers(application: Application) -> None:
    """
    Set up command handlers.
    This method adds command handlers for available commands.

    :param application: Application instance
    :type application: Application
    """

    log.info("Setting up command handlers...")
    available_commands = [cmd for cmd in dir(commands) if cmd.startswith('_command_')]

    async def __add_command_handler(cmd):
        application.add_handler(CommandHandler(cmd[9:], getattr(commands, cmd)))

    await asyncio.gather(*[__add_command_handler(cmd) for cmd in available_commands])
    log.info("Command handlers set up successfully.")


async def _setup_inline_handlers(application: Application) -> None:
    """
    Set up inline handlers.
    This method adds inline query handlers for available inline commands.

    :param application: Application instance
    :type application: Application
    """

    log.info("Setting up inline handlers...")
    available_inline_handlers = [cmd for cmd in dir(inlines) if cmd.startswith('_inline_')]

    async def __add_inline_handler(cmd):
        application.add_handler(InlineQueryHandler(getattr(inlines, cmd)))

    await asyncio.gather(*[__add_inline_handler(cmd) for cmd in available_inline_handlers])
    log.info("Inline handlers set up successfully.")


async def _init_models() -> None:
    """
    Initialize database models.
    This method imports all models from all modules in the BASE_DIR directory and creates all tables in the database.

    :rtype: None
    """

    log.info("Initializing database models...")
    modules = os.listdir(BASE_DIR)
    for module in modules:
        if (os.path.isdir(os.path.join(BASE_DIR, module))
                and os.path.exists(os.path.join(BASE_DIR, module, 'models.py'))):
            __import__(f'{module}.models')

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    log.info("Database models initialized successfully.")


async def post_init(application: Application) -> None:
    """
    Perform post-initialization tasks.
    This method initializes database models, deletes existing bot commands, and sets up command and inline query handlers.

    :param application: Application instance
    :type application: Application
    """

    log.info("Performing post-initialization tasks...")
    await _init_models()
    await application.bot.delete_my_commands()
    await _setup_command_handlers(application)
    await _setup_inline_handlers(application)
    await _setup_commands(application)
    log.info("Post-initialization tasks completed.")


def main():
    """
    Main entry point for the Telegram bot application.
    """

    log.info("Starting the Telegram bot application...")
    app_instance = ApplicationBuilder().token(BOT_TOKEN) \
        .persistence(persistence) \
        .post_init(post_init) \
        .build()

    app_instance.run_polling()


if __name__ == '__main__':
    main()
