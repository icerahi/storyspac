from django.http import HttpResponse
from django.shortcuts import render

# Create your views here.
from rest_framework import permissions
from rest_framework.generics import (
    ListAPIView,
    RetrieveUpdateDestroyAPIView,
    ListCreateAPIView,

)

from api.serializers import PhotoSerializer
from photos.models import Photo


class PhotoAPIView(ListAPIView):
    permission_classes = (permissions.IsAuthenticated,)
    queryset = Photo.objects.all()
    serializer_class = PhotoSerializer

def api_landing(request):
    return HttpResponse('muri khaaa')


class PhotoAPIDetailView(RetrieveUpdateDestroyAPIView):
    permission_classes = (permissions.IsAuthenticated,)

    queryset = Photo.objects.all()
    serializer_class = PhotoSerializer


class PhotoAPICreateView(ListCreateAPIView):
    permission_classes = (permissions.IsAuthenticated,)

    #last photo
    queryset = Photo.objects.all().order_by('-timestamp')[:1]
    serializer_class = PhotoSerializer