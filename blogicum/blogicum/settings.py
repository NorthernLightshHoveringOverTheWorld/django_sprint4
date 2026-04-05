"""Django settings for blogicum project."""

from pathlib import Path

# `BASE_DIR` должен указывать на директорию `blogicum/` (это важно для тестов).
BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = "django-insecure-0@d109%bm_nps_m*ypdw7tjzggz33=e+okh5u$6+mxwj(2gsj)"
DEBUG = True
ALLOWED_HOSTS = []

INSTALLED_APPS = [
    'blog.apps.BlogConfig',  # ТОЛЬКО ТАК!
    'pages.apps.PagesConfig',
    'django_bootstrap5',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "blogicum.urls"

TEMPLATES_DIR = BASE_DIR / "templates"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [TEMPLATES_DIR],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ]
        },
    }
]

WSGI_APPLICATION = "blogicum.wsgi.application"

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

LANGUAGE_CODE = "ru-RU"
TIME_ZONE = "UTC"
USE_I18N = True
# Без этого Django парсит дату/время по форматам из global_settings (ISO, US),
# а не из локали ru — вид «05.04.2026 15:30» не проходит валидацию.
USE_L10N = True
USE_TZ = True

STATIC_URL = '/static/'
STATICFILES_DIRS = [
    BASE_DIR.parent / 'static',
]

MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR.parent / "media"

EMAIL_BACKEND = "django.core.mail.backends.filebased.EmailBackend"
EMAIL_FILE_PATH = BASE_DIR / "sent_emails"

CSRF_FAILURE_VIEW = "pages.views.csrf_failure"

# `django.contrib.auth` по умолчанию редиректит на `/accounts/login/`, тогда как
# в проекте URL входа — под префиксом `auth/` (см. `django.contrib.auth.urls`).
LOGIN_URL = "/auth/login/"
# По умолчанию после входа — `/accounts/profile/`, такого пути в URLconf нет.
LOGIN_REDIRECT_URL = "/"

DEFAULT_AUTO_FIELD = (
    "django.db.models.BigAutoField"
)
