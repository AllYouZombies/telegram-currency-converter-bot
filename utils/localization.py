import gettext

from core.settings import SUPPORTED_LANGS, DEFAULT_LANGUAGE

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


activate_locale()
