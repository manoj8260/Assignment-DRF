from django.urls import path 
from apps.authentication.views import(
     UserRegisterView ,UserAuthenticateView , UserLogoutView , 
)

urlpatterns=[
    path('user/register/',UserRegisterView.as_view(),name='user_register'),
    path('user/login/',UserAuthenticateView.as_view(),name='user_login'),
    path('user/logout/',UserLogoutView.as_view(),name='user_logout'),
   
]