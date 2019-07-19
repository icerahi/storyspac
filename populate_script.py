import os, django


os.environ.setdefault("DJANGO_SETTINGS_MODULE","fame.settings")
django.setup()
from django.contrib.auth.models import User
from django.utils import timezone

import random
from faker import Faker

from articles.models import Article

def create_post(N):
    fake=Faker()
    for _ in range(N):
        id=random.randint(1,4)
        title=fake.name()
        status=random.choice(['published','draft'])

        Article.objects.create(
                                title=title,
                               author=User.objects.get(id=id),
                               slug="-".join(title.lower().split()),
                               body=fake.text(),
                                status=status,
                               created=timezone.now(),
                               updated=timezone.now(),
                               )



create_post(10)
print("Date is genarated")