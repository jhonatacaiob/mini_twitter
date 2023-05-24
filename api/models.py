from django.contrib.auth import get_user_model
from django.db import models


# Create your models here.
class Post(models.Model):
    content = models.CharField(max_length=280)
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
    )
