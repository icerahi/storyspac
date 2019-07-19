from django.urls import path, include

from accounts.views import UserDetailView, UserFollowView,profile_edit

urlpatterns=[

    path('<username>/edit/',profile_edit,name='profile_edit'),
    path('<username>/',UserDetailView.as_view(),name='userdetail'),

    path('<username>/follow/',UserFollowView.as_view(),name='follow')
]