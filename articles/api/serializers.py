from rest_framework.serializers import ModelSerializer,HyperlinkedIdentityField,SerializerMethodField

from articles.models import Article


class ArticleCreateUpdateSerializer(ModelSerializer):
    class Meta:
        model=Article
        fields=('title','body','comment_disable','status',)


article_detail_url=HyperlinkedIdentityField(
        view_name=('articles-api:detail'),
    lookup_field='pk'
    )

article_delete_url=HyperlinkedIdentityField(
    view_name=('articles-api:delete'),
    lookup_field='pk'
)
article_edit_url=HyperlinkedIdentityField(
    view_name=('articles-api:edit'),
    lookup_field='pk'
)


class ArticleDetailSerializer(ModelSerializer):
    detail_url=article_detail_url
    edit_url=article_edit_url
    delete_url=article_delete_url

    user=SerializerMethodField()
   # image=SerializerMethodField()


    class Meta:
        model=Article
        fields = ('detail_url','edit_url','delete_url',
                  'user','title', 'body','comment_disable','liked')


    def get_user(self,obj):
        return str(obj.user.username)

    # def get_image(self,obj):
    #     try:
    #         image=obj.image.url
    #     except:
    #         image=None
    #     return image




class ArticleListSerializer(ModelSerializer):
    detail_url=article_detail_url
    user=SerializerMethodField() # to get username
    class Meta:
        model=Article
        fields = ('detail_url',
                  'user','title', 'body','comment_disable','created')

    def get_user(self,obj):
        return str(obj.user.username)