import os

from django.conf import settings
from django.db import models

# Create your models here.
from django.db.models.signals import post_save, post_delete, m2m_changed
from django.dispatch import receiver
from django.urls import reverse
from django.utils import timezone

from accounts.models import UserProfile
from photos.validators import validate_image



class Photo(models.Model):
    user=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    image=models.ImageField(upload_to='photo/',blank=False,null=False,validators=[validate_image])
    caption=models.CharField(max_length=5000,null=True,blank=True)
    liked =models.ManyToManyField(settings.AUTH_USER_MODEL,blank=True,related_name='liked')
    posted_on=models.DateTimeField(auto_now_add=True)
    timestamp=models.DateTimeField(auto_now_add=True)
    views = models.PositiveIntegerField(default=0, blank=True)



    def __str__(self):
        return (self.caption)

    class Meta:
        ordering=['-timestamp']

    def get_absolute_url(self):
        return reverse('photo:detail',kwargs={"pk":self.pk})

    def get_delete_url(self):
        return reverse('photo:delete',kwargs={"pk":self.pk})

    def get_update_url(self):
        return reverse('photo:update',kwargs={'pk':self.pk})


@receiver(post_delete, sender=Photo)
def auto_delete_on_post_delete(sender, instance, **kwargs):
    if instance.image:
        if os.path.isfile(instance.image.path):
            os.remove(instance.image.path)



class Comment(models.Model):
    photo=models.ForeignKey(Photo,on_delete=models.CASCADE,related_name='commented_photo')
    user=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name='comment_user')
    comment=models.TextField(max_length=160,null=True,blank=True)
    timestamp=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "{} {}".format(self.photo.caption,str(self.user.username))


class Notification(models.Model):
    photo = models.ForeignKey(Photo, on_delete=models.CASCADE, null=True, blank=True)
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE, null=True, blank=True)
    role_user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True)
    profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE, null=True)
    liked = models.BooleanField(default=False, null=True)
    followed = models.BooleanField(default=False, null=True)
    timestamp = models.DateTimeField(auto_now=True,null=True, blank=True)

#create notification for comment
@receiver(post_save,sender=Comment)
def comment_notification(sender,instance,created,**kwargs):
    if created:
        if instance.user !=instance.photo.user:
            Notification.objects.create(photo=instance.photo,comment=instance)


# Creates a notification instance if a post is liked.
@receiver(m2m_changed, sender=Photo.liked.through)
def auto_create_like_notification(sender, instance, action, pk_set, **kwargs):
    if action == "post_add":
        Notification.objects.create(photo=instance, role_user=instance.liked.through.objects.last().user,liked=True)
    if action == "post_remove":
        for num in pk_set:
            pk = num
        Notification.objects.filter(role_user_id=pk, photo=instance).delete()


# Creates a notification instance if a user is followed.
@receiver(m2m_changed, sender=UserProfile.following.through)
def auto_create_follow_notification(sender, instance, action, pk_set, **kwargs):
    if action == "post_add":
        Notification.objects.create(profile=instance, role_user=instance.following.through.objects.last().user,timestamp=timezone.now, followed=True)
    if action == "post_remove":
        for num in pk_set:
            pk = num
        Notification.objects.filter(role_user=pk, profile=instance).delete()