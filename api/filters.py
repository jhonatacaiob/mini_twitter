from django_filters import rest_framework as filters

from api.models import Post

class PostFilter(filters.FilterSet):
    user_id = filters.NumberFilter(field_name='user__id', lookup_expr='exact')

    class Meta:
        model = Post
        fields = ('user_id', )