import secrets
import string

from database.config import settings

ALPHABET = string.ascii_letters + string.digits


def gen_short_code() -> str:
    return "".join(secrets.choice(ALPHABET) for _ in range(settings.DEFAULT_LEN))
