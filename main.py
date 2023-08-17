import os

from telegram.ext import ApplicationBuilder, CommandHandler, Application

from core.db import engine, Base
from core.settings import BOT_TOKEN, persistence, SUPPORTED_LANGS, BASE_DIR
from utils.localization import activate_locale


async def _delete_commands(application: Application) -> None:
    await application.bot.delete_my_commands()


async def _set_commands(application: Application) -> None:
    from bot import commands
    available_commands = (
        cmd for cmd in dir(commands) if cmd.startswith('_command_')
    )

    _commands = []
    for cmd in available_commands:
        application.add_handler(
            CommandHandler(cmd[9:], getattr(commands, cmd))
        )
        _commands.append((cmd[9:], _(cmd[9:])))

    for lang in SUPPORTED_LANGS:
        activate_locale(lang)
        await application.bot.set_my_commands(
            language_code=lang,
            commands=_commands
        )


async def _init_models():
    modules = os.listdir(BASE_DIR)
    for module in modules:
        if os.path.isdir(os.path.join(BASE_DIR, module)) and \
                os.path.exists(os.path.join(BASE_DIR, module, 'models.py')):
            __import__(f'{module}.models')

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


async def post_init(application: Application) -> None:
    await _init_models()
    await _delete_commands(application)
    await _set_commands(application)


def main():
    app_instance = ApplicationBuilder().token(BOT_TOKEN) \
        .persistence(persistence) \
        .post_init(post_init) \
        .build()

    app_instance.run_polling()


if __name__ == '__main__':
    main()
