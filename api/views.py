from rest_framework import permissions
from rest_framework.generics import CreateAPIView
from django.contrib.auth.models import User
from api.serializers import UserSerializer


class CreateUserView(CreateAPIView):
    model = User
    permission_classes = [permissions.AllowAny]
    serializer_class = UserSerializer


def sample_view(request):
    current_user = request.user
    if current_user.is_authenticated:
        print(current_user)
