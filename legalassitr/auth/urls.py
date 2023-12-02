from django.urls import include, path
from rest_framework import routers
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import *

urlpatterns = [
    path('token/', TokenObtainPairView.as_view(), name='token_obtain'),
    path('register/', RegistrationView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('fgpass', ForgotPasswordView.as_view(), name='forgot_password'),
    path('passreset/<uid_b64>/<token>/', PasswordResetView.as_view(), name='password_reset')
]