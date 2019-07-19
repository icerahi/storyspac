from django.contrib import admin

# Register your models here.
from articles.models import Article, Images, Comment


class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title','slug','user','status')
    list_filter = ('status','created','updated')
    search_fields = ('author__username','title')

    prepopulated_fields = {'slug': ('title',)}
    list_editable = ('status',)
    date_hierarchy = ('created')

class ImagesAdmin(admin.ModelAdmin):
    list_display = ('article','image')




admin.site.register(Article,ArticleAdmin)
admin.site.register(Images,ImagesAdmin)
admin.site.register(Comment)