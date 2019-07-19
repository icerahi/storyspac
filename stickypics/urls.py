from django.urls import path

from stickypics.views import StickypicCreateAndListView, stickypic_detail, StickypicUpdateView, StickypicDeleteView, \
    like_post

urlpatterns = [
    path('',StickypicCreateAndListView.as_view(),name='stickylist'),
    path('<int:pk>',stickypic_detail,name='stickydetail'),
    path('<int:pk>/update',StickypicUpdateView.as_view(),name='stickyupdate'),
    path('like/',like_post,name='like_post'),
    path('<int:pk>/delete',StickypicDeleteView.as_view(),name='stickydelete')



]
