from django.db import models
from django.contrib.auth import get_user_model

# Create your models here.
class Post(models.Model):
    content = models.CharField(max_length=280)
    created_at = models.DateTimeField(auto_now_add=True)
    user_id = models.ForeignKey(
        get_user_model(),
        on_delete=models.CASCADE,
    )
