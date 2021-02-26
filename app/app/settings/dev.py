from .base import *


DEBUG = os.getenv("DEBUG", 1)

ALLOWED_HOSTS = os.environ.get("ALLOWED_HOSTS").split(" ")
CORS_ALLOWED_ORIGINS = os.environ.get("CORS_ALLOWED_ORIGINS").split(" ")
