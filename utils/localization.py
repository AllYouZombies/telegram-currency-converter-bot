import gettext

from core.settings import SUPPORTED_LANGS, DEFAULT_LANGUAGE, LOCALE_DIR

translations = {}

for lang in SUPPORTED_LANGS:
    translations[lang] = gettext.translation('messages', localedir='locale', languages=[lang])


def activate_locale(language_code: str = DEFAULT_LANGUAGE) -> None:
    """
    Activate locale for current language code
    :param language_code: code of language to activate. Default is DEFAULT_LANGUAGE. Choices are SUPPORTED_LANGS
    :return: Nothing
    """

    if language_code not in SUPPORTED_LANGS:
        language_code = DEFAULT_LANGUAGE
    translations[language_code].install(names=['gettext', 'ngettext'])


try:
    _(None)
except NameError:
    activate_locale()


def translate(msg_to_translate, get_ori=False):
    current_lang = gettext._current_domain

    if current_lang not in SUPPORTED_LANGS:
        current_lang = DEFAULT_LANGUAGE

    def find_key(lang_code):
        items = translations[lang_code]._catalog.items()
        for key, value in items:
            if value == msg_to_translate:
                return key
        return None

    if get_ori:
        orig = find_key(current_lang) or find_key(DEFAULT_LANGUAGE) or msg_to_translate
        return orig
    else:
        translated = translations[current_lang].gettext(msg_to_translate)
        return translated
