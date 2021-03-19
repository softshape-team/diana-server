from app.app.settings.ci import DEBUG
from .base import *


DEBUG = False

SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
