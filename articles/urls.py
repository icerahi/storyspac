from django.urls import path

from articles.views import(
 article_list,
 article_detail,
 article_create,
 like_post,
 article_delete
, article_edit,
favourite,)

urlpatterns = [
   path('',article_list,name='list'),
    path('<int:id>/edit/',article_edit,name='edit'),
    path('<int:id>/delete/',article_delete,name='delete'),
    path('<int:pk>/<slug>/',article_detail,name='detail'),
    path('create/',article_create,name='create'),

    path('like/',like_post,name="like_post"),
    path('favourite/<int:id>/',favourite,name='favourite'),
     ]
