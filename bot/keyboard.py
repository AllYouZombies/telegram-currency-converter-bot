from telegram import KeyboardButton, ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton


async def get_kb(buttons: list[list[str] | str],
                 resize_keyboard: bool = True,
                 one_time_keyboard: bool = False,
                 *args, **kwargs) -> ReplyKeyboardMarkup:
    keyboard = []
    for item in buttons:
        if isinstance(item, list):
            row = []
            for button in item:
                row.append(KeyboardButton(button))
            keyboard.append(row)
        else:
            keyboard.append([KeyboardButton(item)])
    return ReplyKeyboardMarkup(keyboard, resize_keyboard, one_time_keyboard, *args, **kwargs)


async def get_inline_kb(buttons: list[tuple[str, str] | list[tuple[str, str]]],
                        *args, **kwargs) -> InlineKeyboardMarkup:
    keyboard = []
    for item in buttons:
        if isinstance(item, list):
            row = []
            for button in item:
                row.append(InlineKeyboardButton(button[0], callback_data=button[1]))
            keyboard.append(row)
        else:
            keyboard.append([InlineKeyboardButton(item[0], callback_data=item[1])])
    return InlineKeyboardMarkup(keyboard, *args, **kwargs)
