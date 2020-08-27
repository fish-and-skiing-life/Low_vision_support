from webapi.models import Profile
from webapi.serializers import ProfileSerializer
from rest_framework import generics
from rest_framework import views
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .lib import crawling

class ProfileListCreate(generics.ListCreateAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
