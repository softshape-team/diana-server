from .base import *

DEBUG = True

ALLOWED_HOSTS = "*"

CORS_ALLOWED_ORIGINS = os.environ.get("CORS_ALLOWED_ORIGINS").split(" ")
