from django.contrib.auth.models import User
from django.forms.models import model_to_dict
from rest_framework import permissions
from rest_framework.generics import CreateAPIView, ListCreateAPIView
from rest_framework.response import Response
from rest_framework.status import HTTP_201_CREATED

from api.pagination import PostPagination
from api.serializers import PostSerializer, UserSerializer

from .filters import PostFilter
from .models import Post


class CreateUserView(CreateAPIView):
    model = User
    permission_classes = (permissions.AllowAny,)
    serializer_class = UserSerializer


class PostView(ListCreateAPIView):
    model = Post
    serializer_class = PostSerializer
    permission_classes = (permissions.IsAuthenticated,)
    pagination_class = PostPagination
    filterset_class = PostFilter

    def get_queryset(self):
        user_id = self.request.user.id
        return Post.objects.exclude(user_id=user_id)

    def create(self, request, *args, **kwargs):
        user = self.request.user
        content = request.data['content']

        p = Post(content=content, user=user)
        p.save()
        return Response(
            {
                'id': p.id,
                'content': p.content,
                'user': p.user.username,
            },
            status=HTTP_201_CREATED,
        )
