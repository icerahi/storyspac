from django.contrib import admin

# Register your models here.
from accounts.models import UserProfile

class Profile(admin.ModelAdmin):
    list_display = ['user','fullname','profile_pic','date_of_birth']
    search_fields = ['user','fullname','date_of_birth']
admin.site.register(UserProfile,Profile)