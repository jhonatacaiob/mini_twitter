from django.urls import path
from django.views.decorators.csrf import csrf_exempt
from .views import CreateUserView

urlpatterns = [
    path('create_user/', csrf_exempt(CreateUserView.as_view())),
]