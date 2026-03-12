from django.urls import path

from users.views import (
    RegisterFormView,
    LoginView,
    LogoutView,
    AccountView,
    ResetPasswordView,
    VerifyEmailView
)

app_name = 'users'

urlpatterns = [
    path('register/', RegisterFormView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('account/', AccountView.as_view(), name='account'),
    path('reset-password/', ResetPasswordView.as_view(), name='reset-password'),
    path('verify-email/<uidb64>/<token>/', VerifyEmailView.as_view(), name='verify-email'),
]