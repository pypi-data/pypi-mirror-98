from pyUltroid import *
from ..dB.database import Var
from .parser.google import GoogleSearch
from .parser.yahoo import YahooSearch

DANGER = [
    "APP_ID",
    "API_HASH",
    "SESSION",
    "BOT_TOKEN",
    "HEROKU_API",
    "base64",
    "base32",
    "get_me",
    "NewMessage",
    "REDIS_PASSWORD",
    "load_addons",
    "load_plugins",
]
