from django.urls import include, path
from .views import *

urlpatterns = [
    path('register/', UserRegisterationView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('profile/', UserView.as_view(), name='profile'),
    path('fgpass', ForgotPasswordView.as_view(), name='forgot_password'),
    path('passreset/', PasswordResetView.as_view(), name='password_reset'),
    path('verifyotp/', VerifyOTPView.as_view(), name='verifyotp')
]
