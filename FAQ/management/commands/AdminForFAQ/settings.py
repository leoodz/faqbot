import os
DEBUG=True
#ROOT_URLCONF = 'AdminForFAQ.urls'
ROOT_URLCONF = 'AdminForFAQ.urls'
ALLOWED_HOSTS = [
  'https://faqbot.leoodz.repl.co',
  'b00b9f5b-9e44-40a2-9890-82f8628e4eb2.id.repl.co',
  'faqbot.leoodz.repl.co',
]
CSRF_TRUSTED_ORIGINS = [
  'https://faqbot.leoodz.repl.co','https://*.127.0.0.1'
]
SECRET_KEY='54heg!3=i#1puqy7qkd8qbu_)y!xmpts4v^s^5zd4!pk1wnpnc'
INSTALLED_APPS = [
'django.contrib.admin',
'django.contrib.messages',
'django.contrib.staticfiles',
'django.contrib.contenttypes',
'django.contrib.sessions',
'django.contrib.auth',
'FAQ',
'AdminForFAQ',
'account',
'debug_toolbar',
]

MIDDLEWARE = [
'django.contrib.sessions.middleware.SessionMiddleware',
'django.contrib.messages.middleware.MessageMiddleware',
'django.contrib.auth.middleware.AuthenticationMiddleware',
'debug_toolbar.middleware.DebugToolbarMiddleware',
]

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'bpaxz9yjjsutqfqywdqg',
        'USER': 'unwvzhdmdpwnir2v',
        'PASSWORD': 'uI3OYyX6rmbBADsW36sl',
        'HOST': 'bpaxz9yjjsutqfqywdqg-mysql.services.clever-cloud.com',
        'PORT': '3306',
        'OPTIONS': {
            'init_command': "SET sql_mode='STRICT_TRANS_TABLES'",  # Strict mode
        },
    }
}

STATIC_URL = '/static/'
BASE_DIR = 'C:/Users/leoodz/FAQTelegramBotWithAdmin'
STATICFILES_DIRS = (
     os.path.join(BASE_DIR, 'C:/Users/leoodz/FAQTelegramBotWithAdmin/FAQ/static/'),
     os.path.join(BASE_DIR, 'C:/Users/leoodz/FAQTelegramBotWithAdmin/account/static/'),
 )

STATIC_ROOT = os.path.join(BASE_DIR, 'static')