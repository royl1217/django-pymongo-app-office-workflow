"""
Django settings for config project.
"""

import os
from pathlib import Path
from mongoengine import connect
from dotenv import load_dotenv

load_dotenv()


# ---------------------------------------------------------
# Paths
# ---------------------------------------------------------
BASE_DIR = Path(__file__).resolve().parent.parent

# ---------------------------------------------------------
# Security
# ---------------------------------------------------------
SECRET_KEY = 'django-insecure-v8anp^ea&$mlddd576*&pq#lc+04nxr+%9lyyppr+$9@#%85_4'
DEBUG = True
ALLOWED_HOSTS = []

# ---------------------------------------------------------
# Installed Apps
# ---------------------------------------------------------
INSTALLED_APPS = [
  "django.contrib.auth",
  "django.contrib.contenttypes",
  "django.contrib.sessions",
  "django.contrib.messages",
  "django.contrib.staticfiles",

  "workflow",   # ← ADD THIS BACK
]

# ---------------------------------------------------------
# Middleware
# ---------------------------------------------------------
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "config.urls"

# ---------------------------------------------------------
# Templates
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
# Django Internal Database (SQLite)
# ---------------------------------------------------------
# Django *must* have a SQL database for sessions, middleware, etc.
# This database does NOT store your app data.
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}

# ---------------------------------------------------------
# MongoDB (MongoEngine)
# ---------------------------------------------------------
MONGODB_URI = os.getenv("MONGO_DB_URI")
MONGODB_NAME = os.getenv("MONGO_DB_NAME", "workflowDemo")

connect(
    db=MONGODB_NAME,
    host=MONGODB_URI,
)

# ---------------------------------------------------------
# Internationalization
# ---------------------------------------------------------
LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True

# ---------------------------------------------------------
# Static Files
# ---------------------------------------------------------
STATIC_URL = "static/"