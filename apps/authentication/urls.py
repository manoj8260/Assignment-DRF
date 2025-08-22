from django.urls import path
from apps.authentication.views import (
    UserRegisterView,
    UserAuthenticateView,
    UserLogoutView,
)

urlpatterns = [
    # Endpoint for user registration
    path('user/register/', UserRegisterView.as_view(), name='user_register'),

    # Endpoint for user login/authentication
    path('user/login/', UserAuthenticateView.as_view(), name='user_login'),

    # Endpoint for user logout (blacklists refresh token)
    path('user/logout/', UserLogoutView.as_view(), name='user_logout'),
]
