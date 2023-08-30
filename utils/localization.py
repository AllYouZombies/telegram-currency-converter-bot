import logging
import gettext
gettext.translation('messages', localedir='locale', languages=['en']).install(names=['gettext', 'ngettext'])

from core.settings import SUPPORTED_LANGS, DEFAULT_LANGUAGE


logging = logging.getLogger(__name__)

translations = {}

for code, name in SUPPORTED_LANGS:
    translations[code] = gettext.translation('messages', localedir='locale', languages=[code])


def activate_locale(language_code: str = DEFAULT_LANGUAGE) -> None:
    """
    Activate locale for current language code
    :param language_code: code of language to activate. Default is DEFAULT_LANGUAGE. Choices are SUPPORTED_LANGS
    :return: Nothing
    """

    if language_code not in (i[0] for i in SUPPORTED_LANGS):
        language_code = DEFAULT_LANGUAGE
    translations[language_code].install(names=['gettext', 'ngettext'])


try:
    _(None)
except NameError:
    activate_locale()


def rev_translate(translated_msg):
    current_lang = gettext._current_domain

    if current_lang not in (i[0] for i in SUPPORTED_LANGS):
        current_lang = DEFAULT_LANGUAGE

    def find_key(lang_code):
        items = translations[lang_code]._catalog.items()
        for key, value in items:
            if value == translated_msg or value == translated_msg:
                return key
        return None

    orig = find_key(current_lang) or find_key(DEFAULT_LANGUAGE) or translated_msg
    return orig
