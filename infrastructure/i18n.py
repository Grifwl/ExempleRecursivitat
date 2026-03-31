"""Internationalisation (i18n) configuration.

Importing this module installs the _() translation function as a Python
built-in, making it available throughout the project without explicit imports.

Environment variables (loaded from .env if python-dotenv is installed):
    LANG: Language code to use, e.g. 'ca', 'en', 'es'. Defaults to 'en'.
          Only the language part is used; locale suffixes like '_ES' are ignored.

Supported languages must have a compiled .mo file under:
    locales/<lang>/LC_MESSAGES/hanoi.mo
"""

import builtins
import gettext
import logging
import os
from pathlib import Path

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

log = logging.getLogger(__name__)

_LOCALES_DIR = Path(__file__).parent.parent / "locales"


def _configure() -> None:
    """Loads the translation catalogue and installs _() as a built-in.

    Falls back to returning the original string if no catalogue is found
    for the requested language, so the application always runs even without
    compiled translation files.
    """
    lang = os.getenv("LANG", "en").split("_")[0].split(".")[0]

    try:
        translation = gettext.translation(
            domain="hanoi",
            localedir=_LOCALES_DIR,
            languages=[lang],
        )
        translation.install()
        log.debug("Loaded translations for language: %s", lang)
    except FileNotFoundError:
        gettext.install("hanoi")
        log.debug("No translations found for '%s', using original strings", lang)


_configure()
