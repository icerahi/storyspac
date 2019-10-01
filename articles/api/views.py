from rest_framework.generics import ListAPIView, RetrieveAPIView, UpdateAPIView, DestroyAPIView, RetrieveUpdateAPIView, \
    RetrieveDestroyAPIView, CreateAPIView
from rest_framework.permissions import AllowAny
from articles.api.serializers import ArticleListSerializer, ArticleDetailSerializer, ArticleCreateUpdateSerializer
from articles.models import Article
from rest_framework.permissions import (
AllowAny,
IsAdminUser,
IsAuthenticated
)
from .permissions import IsOwnerOrReadOnly
from rest_framework.filters import SearchFilter,OrderingFilter

class ArticleCreateAPIView(CreateAPIView):
    queryset = Article.objects.all()
    serializer_class = ArticleCreateUpdateSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class ArticleDetailAPIView(RetrieveAPIView):
    queryset = Article.published.all()
    serializer_class = ArticleDetailSerializer
    permission_classes = [IsAuthenticated]
    #lookup_field = 'slug'
    #lookup_url_kwarg = 'slug'

class ArticleUpdateAPIView(RetrieveUpdateAPIView):
    queryset = Article.published.all()
    serializer_class = ArticleCreateUpdateSerializer
    permission_classes = [IsAuthenticated,IsOwnerOrReadOnly]

    def perform_update(self, serializer):
        serializer.save(user=self.request.user)



class ArticleDeleteAPIView(DestroyAPIView):
    queryset = Article.objects.all()
    serializer_class = ArticleDetailSerializer
    permission_classes = [IsAuthenticated,IsOwnerOrReadOnly]


#no pagination
class ArticleListAPIView(ListAPIView):
    serializer_class = ArticleListSerializer
    permission_classes = [IsAuthenticated]
    filter_backends = [SearchFilter,OrderingFilter]
    search_fields=['title','body','user__username']

    def get_queryset(self):
        queryset=Article.objects.all()
        following_post = self.request.user.profile.get_following()
        qs1 = Article.published.filter(user__in=following_post)
        qs2 = Article.published.filter(user=self.request.user)
        queryset = (qs1 | qs2).distinct()
        return queryset


