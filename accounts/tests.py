from django.contrib.auth import get_user_model
from django.test import TestCase

# Create your tests here.
from .models import UserProfile
User=get_user_model()

class UserProfileTestCase(TestCase):

    def setup(self):
        self.username="some_user"
        new_user=User.objects.create(username=self.username)

    def test_profile_created(self):
        username = self.username
        user_profile = UserProfile.object.filter(user__username=username)
        print(user_profile)
        self.assertTrue(user_profile.exists())
        self.assertTrue(user_profile.count() == 1)