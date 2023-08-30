from telegram import Update, ReplyKeyboardRemove
from telegram.ext import ContextTypes

from bot.menus.language import menu_language
from bot.menus.main import menu_main
from bot.utils import description, assign_user_and_localize, show_typing


@description(_('🚀 Restart the bot'))
@show_typing()
@assign_user_and_localize()
async def command_start(update: Update, context: ContextTypes.DEFAULT_TYPE, user, *args, **kwargs) -> None:
    # Remove existing keyboard
    restart_msg = await update.message.reply_text(_('Restarting the bot...'), reply_markup=ReplyKeyboardRemove())
    # Clear user_data and chat_data
    context.user_data.clear()
    context.chat_data.clear()
    await restart_msg.delete()
    return await menu_main(update, context, user, *args, **kwargs)


@description(_('🌍 Language'))
@show_typing()
@assign_user_and_localize()
async def command_language(*args, **kwargs) -> None:
    return await menu_language(*args, **kwargs)
