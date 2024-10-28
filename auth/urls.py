from auth.views import MyObtainTokenPairView, RegisterView, getUser
from rest_framework_simplejwt.views import (
    TokenRefreshView,
)
from django.urls import path


urlpatterns = [
    path('token/', MyObtainTokenPairView.as_view(), name = 'token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name = 'token_refresh'),
    
    path('register/', RegisterView.as_view(), name = 'auth_register'),
    path('user/', getUser, name = 'get_user'),
]