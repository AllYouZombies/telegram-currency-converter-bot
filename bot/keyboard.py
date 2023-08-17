from telegram import KeyboardButton, ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import ExtBot


class Keyboard:

    async def get_kb(self, buttons: list[list[str] | str]) -> ReplyKeyboardMarkup:
        keyboard = []
        for button in buttons:
            keyboard.append([KeyboardButton(button)])
        return ReplyKeyboardMarkup(keyboard)

    async def get_inline_kb(self, buttons: list[tuple[str, str] | list[tuple[str, str]]]) -> InlineKeyboardMarkup:
        keyboard = []
        for item in buttons:
            if isinstance(item, list):
                row = []
                for button in item:
                    row.append(InlineKeyboardButton(button[0], callback_data=button[1]))
                keyboard.append(row)
            else:
                keyboard.append([InlineKeyboardButton(item[0], callback_data=item[1])])
        return InlineKeyboardMarkup(keyboard)
