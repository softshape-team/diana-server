from .base import *

DEBUG = True

ALLOWED_HOSTS = "*"

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": os.getenv("POSTGRESQL_DB"),
        "HOST": os.getenv("POSTGRESQL_HOST", "localhost"),
        "PORT": os.getenv("POSTGRESQL_PORT", 5432),
        "USER": os.getenv("POSTGRESQL_USER"),
        "PASSWORD": os.getenv("POSTGRESQL_PASSWORD"),
    }
}
