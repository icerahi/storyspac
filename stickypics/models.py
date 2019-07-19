from django.conf import settings
from django.db import models

# Create your models here.
from django.urls import reverse





class Stickypic(models.Model):
    user=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    image=models.ImageField(upload_to='stickypic/',blank=False,null=False)
    description=models.CharField(max_length=5000,null=True,blank=True)
    source=models.URLField(max_length=250,null=False,blank=False)

    liked =models.ManyToManyField(settings.AUTH_USER_MODEL,blank=True,related_name='stickypic_liked')
    update_at=models.DateTimeField(auto_now=True)
    timestamp=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.source
    class Meta:
        ordering=['-timestamp']

    def get_absolute_url(self):
        return reverse('stickypic:stickydetail',kwargs={'pk':self.pk})

    def get_update_url(self):
        return reverse('stickypic:stickyupdate',kwargs={'pk':self.pk})

    def get_delete_url(self):
        return reverse('stickypic:stickydelete',kwargs={'pk':self.pk})


    def __str__(self):
        return (self.source)

    class Meta:
        ordering=['-update_at']



class Comment(models.Model):
    stickypic=models.ForeignKey(Stickypic,on_delete=models.CASCADE,related_name='commented_stickypic')
    user=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE,related_name='stickypic_comment_user')
    comment=models.TextField(max_length=160,null=True,blank=True)
    update_at = models.DateTimeField(auto_now=True)
    timestamp=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "{} {}".format(self.stickypic.source,str(self.user.username))