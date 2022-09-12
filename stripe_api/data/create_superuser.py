import os

import django
from django.core.wsgi import get_wsgi_application

# Внимательно тут!!!
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'stripe_api.settings')
django.setup()
application = get_wsgi_application()


from django.contrib.auth.models import User

users = User.objects.all()
if not users:
    User.objects.create_superuser(username="superuser",
                                  email="user@example.com",
                                  password="password",
                                  is_active=True,
                                  is_staff=True)
    print('Суперпользователь создан! username = superuser password = password')
else:
    print('Суперюзер не создан, уже есть пользователи.')
