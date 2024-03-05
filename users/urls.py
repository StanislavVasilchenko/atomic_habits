from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from users.apps import UsersConfig
from users.views import UserRegisterAPIView, UserRetrieveAPIView, UserUpdateAPIView

app_name = UsersConfig.name

urlpatterns = [
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # user
    path('register/', UserRegisterAPIView.as_view(), name='user_register'),
    path('profile/<int:pk>/', UserRetrieveAPIView.as_view(), name='user-profile'),
    path('update/<int:pk>/', UserUpdateAPIView.as_view(), name='user-update-profile'),
]