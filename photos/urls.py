
from django.urls import path

from photos.views import (
    photo_detail,

    PhotoCreateAndListView,
    PhotoUpdateView,
    PhotoDeleteView,
    like_post, ViewNotifications)

urlpatterns = [
    path('',PhotoCreateAndListView.as_view(),name='list'),

   # path('',PhotoListView.as_view(),name='list'),
    path('<int:pk>/',photo_detail,name='detail'),
    path('like/',like_post,name='like_post'),
    path('<int:pk>/update',PhotoUpdateView.as_view(),name='update'),
    path('<int:pk>/delete',PhotoDeleteView.as_view(),name='delete'),

    path('notification/',ViewNotifications.as_view(),name='notification'),


]

