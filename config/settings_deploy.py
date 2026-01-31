import os
from pathlib import Path
from dotenv import load_dotenv
from mongoengine import connect
from django.utils import timezone

# Load .env variables (Render injects them automatically)
load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent

# ---------------------------------------------------------
# SECURITY
# ---------------------------------------------------------
SECRET_KEY = os.getenv("DJANGO_SECRET_KEY", "fallback-secret-key")
DEBUG = os.getenv("DEBUG", "False") == "True"

ALLOWED_HOSTS = ["*"]  # Render assigns dynamic hostnames

# ---------------------------------------------------------
# INSTALLED APPS
# ---------------------------------------------------------
INSTALLED_APPS = [
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",

    "workflow",  # your app
]

# ---------------------------------------------------------
# MIDDLEWARE
# ---------------------------------------------------------
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
]

ROOT_URLCONF = "config.urls"

# ---------------------------------------------------------
# TEMPLATES
# ---------------------------------------------------------
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.template.context_processors.static",
                "django.template.context_processors.media",
                "django.template.context_processors.tz",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "config.wsgi.application"

# ---------------------------------------------------------
# DATABASE — MongoEngine (Atlas)
# ---------------------------------------------------------
MONGODB_URI = os.getenv("MONGO_DB_URI")
MONGODB_NAME = os.getenv("MONGO_DB_NAME", "workflowDemo")

if not MONGODB_URI:
    raise Exception("Missing MONGO_DB_URI — set it in Render environment variables.")

connect(
    db=MONGODB_NAME,
    host=MONGODB_URI,
)

# ---------------------------------------------------------
# PASSWORD VALIDATION (not used but required by Django)
# ---------------------------------------------------------
AUTH_PASSWORD_VALIDATORS = []

# ---------------------------------------------------------
# INTERNATIONALIZATION
# ---------------------------------------------------------
LANGUAGE_CODE = "en-us"
TIME_ZONE = "Asia/Hong_Kong"
USE_I18N = True
USE_L10N = True
USE_TZ = True

# ---------------------------------------------------------
# STATIC FILES (Render serves from /staticfiles)
# ---------------------------------------------------------
STATIC_URL = "/static/"
STATIC_ROOT = os.path.join(BASE_DIR, "staticfiles")

STATICFILES_DIRS = [
    os.path.join(BASE_DIR, "workflow/static"),
]

# ---------------------------------------------------------
# SESSION SETTINGS
# ---------------------------------------------------------
SESSION_ENGINE = "django.contrib.sessions.backends.signed_cookies"
SESSION_COOKIE_AGE = 60 * 60 * 24 * 7  # 7 days

# ---------------------------------------------------------
# DEFAULT PRIMARY KEY FIELD TYPE
# ---------------------------------------------------------
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"