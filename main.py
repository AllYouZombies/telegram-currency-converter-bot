import os

from telegram.ext import ApplicationBuilder, CommandHandler, Application, InlineQueryHandler

from bot.inline import inline_query
from core.db import engine, Base
from core.settings import BOT_TOKEN, persistence, SUPPORTED_LANGS, BASE_DIR
from utils.localization import activate_locale, rev_translate
from bot import commands
from converter.tasks import retrieve_exchage_rates


async def _set_commands(application: Application) -> None:
    """
    Set bot commands. This method is called after bot initialization.
    Import all commands from bot/commands.py and set them as bot commands.

    :param application: Application instance
    """

    for lang in SUPPORTED_LANGS:
        activate_locale(lang)
        available_commands = list(
            cmd for cmd in dir(commands) if cmd.startswith('_command_')
        )
        _commands = list(
            (cmd[9:], _(rev_translate(getattr(commands, cmd).__doc__)))
            for cmd in available_commands
        )
        await application.bot.set_my_commands(
            language_code=lang,
            commands=_commands
        )


async def _set_command_handlers(application: Application) -> None:
    available_commands = list(
        cmd for cmd in dir(commands) if cmd.startswith('_command_')
    )

    for cmd in available_commands:
        application.add_handler(CommandHandler(cmd[9:], getattr(commands, cmd)))


async def _init_models() -> None:
    """
    Import all models from app/models.py and create tables in database.
    """

    modules = os.listdir(BASE_DIR)
    for module in modules:
        if os.path.isdir(os.path.join(BASE_DIR, module)) and \
                os.path.exists(os.path.join(BASE_DIR, module, 'models.py')):
            __import__(f'{module}.models')

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def post_init(application: Application) -> None:
    await _init_models()
    await application.bot.delete_my_commands()
    await _set_command_handlers(application)
    application.add_handler(InlineQueryHandler(inline_query))
    await _set_commands(application)


def main():
    app_instance = ApplicationBuilder().token(BOT_TOKEN) \
        .persistence(persistence) \
        .post_init(post_init) \
        .build()

    # retrieve_exchage_rates.delay()

    app_instance.run_polling()


if __name__ == '__main__':
    main()

