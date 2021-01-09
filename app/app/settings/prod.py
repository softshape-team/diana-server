from .base import *

DEBUG = os.getenv("DEBUG", 0)

ALLOWED_HOSTS = os.environ.get("ALLOWED_HOSTS").split(" ")
