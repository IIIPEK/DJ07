from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register_user, name='register'),
    path('userinfo/<int:user_id>/', views.user_info, name='user_info'),
]