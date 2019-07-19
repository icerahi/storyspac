from django.conf import settings
from django.db import models

# Create your models here.
from django.db.models.signals import post_save
from django.urls import reverse

class UserProfileManager(models.Manager):
    use_for_releted_fields=True
    def all(self):
        qs=self.get_queryset().all()
        try:
            if self.instance:
                qs = qs.exclude(user=self.instance)
        except:
            pass
        return qs

    def toggle_follow(self,user,to_toggle_user):
        user_profile,created=UserProfile.object.get_or_create(user=user)
        if to_toggle_user in user_profile.following.all():
            user_profile.following.remove(to_toggle_user)
            added=False
        else:
            user_profile.following.add(to_toggle_user)
            added=True
        return added

    def is_following(self,user,followed_by_user):
        user_profile,created=UserProfile.object.get_or_create(user=user)
        if created:
            return False
        if followed_by_user in user_profile.following.all():
            return True
        return False

    def recommended(self,user):
        profile=user.profile
        following=profile.following.all()
        following=profile.get_following()
        qs=self.get_queryset().exclude(user__in=following).exclude(id=profile.id)

        return qs


class UserProfile(models.Model):
    user        =models.OneToOneField(settings.AUTH_USER_MODEL,unique=True,related_name='profile',on_delete=models.CASCADE)
    fullname    =models.CharField(max_length=200,blank=True,null=True)
    profile_pic =models.ImageField(upload_to='profile/',blank=True,null=True,verbose_name="profile_pic",default='default.png')
    date_of_birth=models.DateField(null=True,blank=True)
    bio         =models.CharField(max_length=200,blank=True,null=True)
    following   =models.ManyToManyField(settings.AUTH_USER_MODEL,blank=True,related_name='followed_by')
    object =UserProfileManager()

    def __str__(self):
        return str(self.following.all().count())

    def get_following(self):
        users =self.following.all()
        return users.exclude(username=self.user)

    def get_follow_url(self):
        return reverse('profile:follow',kwargs={'username':self.user.username})



def post_save_user_receiver(sender,instance,created,*args,**kwargs):
    #user will saved as profile
    if created:
        new_profile=UserProfile.object.get_or_create(user=instance)

post_save.connect(post_save_user_receiver,sender=settings.AUTH_USER_MODEL)