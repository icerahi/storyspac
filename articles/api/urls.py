from django.urls import path

from articles.api.views import ArticleDetailAPIView, ArticleListAPIView, ArticleDeleteAPIView, ArticleUpdateAPIView, \
  ArticleCreateAPIView

urlpatterns = [
    path('',ArticleListAPIView.as_view(),name='list'),
    path('<int:pk>/',ArticleDetailAPIView.as_view(),name='detail'),
    path('<int:pk>/delete/',ArticleDeleteAPIView.as_view(),name='delete'),
    path('<int:pk>/edit/',ArticleUpdateAPIView.as_view(),name='edit'),
    path('create',ArticleCreateAPIView.as_view(),name='create'),
    #
    # path('like/',like_post,name="like_post"),
    # path('favourite/<int:id>/',favourite,name='favourite'),
    #
  ]