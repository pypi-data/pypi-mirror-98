from tempfile import mkdtemp

SECRET_KEY = 'fake-key'
INSTALLED_APPS = [
    'tests',
    'django_imbue_tag'
]
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': ':memory:',
    }
}
TEMPLATE_DIR = mkdtemp()
TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            TEMPLATE_DIR
        ],
    },
]