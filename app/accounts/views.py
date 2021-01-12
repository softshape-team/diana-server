from django.contrib.auth import get_user_model
from rest_framework import generics

from .serializers import RegistrationSerializer


User = get_user_model()


class Registration(generics.CreateAPIView):
    serializer_class = RegistrationSerializer
