from django.urls import path
from .views import PhotoAPIView,PhotoAPIDetailView,PhotoAPICreateView
from .views import api_landing

urlpatterns=[
    path('',api_landing,name='api-landing'),
    path('photos/',PhotoAPIView.as_view(),name='photo-list'),
    path('photos/<int:pk>/',PhotoAPIDetailView.as_view(),name='photo-detail'),
    path('photos/new/',PhotoAPICreateView.as_view(),name='photo-create'),


]