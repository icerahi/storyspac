from django.conf import settings
from django.contrib.auth.models import User
from django.db import models

# Create your models here.
from django.db.models.signals import pre_save
from django.urls import reverse
from django.dispatch import receiver
from django.utils.text import slugify


class PublishedManager(models.Manager):
    def get_queryset(self):
        return super(PublishedManager, self).get_queryset().filter(status='published')

class Article(models.Model):
    STATUS_CHOICES=(
        ('draft','Draft'),
        ('published','Published')
    )

    title= models.CharField(max_length=100)
    slug= models.SlugField(max_length=120)
    user= models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    body=models.TextField()
    created=models.DateTimeField(auto_now_add=True)
    updated=models.DateTimeField(auto_now=True)
    status=models.CharField(max_length=10,choices=STATUS_CHOICES,default='draft')

    published=PublishedManager() # costom model manager
    liked=models.ManyToManyField(settings.AUTH_USER_MODEL,related_name="article_liked",blank=True)

    objects=models.Manager() # default manage
    comment_disable=models.BooleanField(default=False)

    favourite=models.ManyToManyField(settings.AUTH_USER_MODEL,blank=True,related_name='favourite')
    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('article:detail', kwargs={'pk':self.id,'slug':self.slug})
    def get_edit_url(self):
        return reverse('article:edit', kwargs={'id':self.id})

    def get_delete_url(self):
        return reverse('article:delete', kwargs={'id': self.id})


@receiver(pre_save,sender=Article)
def pre_save_slug(sender,**kwargs):
    slug=slugify(kwargs['instance'].title)
    kwargs['instance'].slug=slug

class Images(models.Model):
    article=models.ForeignKey(Article,on_delete=models.CASCADE)
    image=models.ImageField(upload_to="articles/",blank=True,null=True)

    def __str__(self):
        return self.article.title + "Image"



class Comment(models.Model):
    article=models.ForeignKey(Article,on_delete=models.CASCADE)
    user=models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    reply=models.ForeignKey('Comment',on_delete=models.CASCADE,null=True,related_name='replies')
    comment=models.TextField(max_length=160,null=True,blank=True)
    timestamp=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return "{} - {}".format(self.article.title,self.user.username)





















