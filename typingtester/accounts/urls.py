from django.urls import path  # , include

from .views import (CheckIfAuthenticated, EmailVerificationView, LoginView,
                    LogoutView, PasswordResetConfirmView, RegistrationView,
                    ResetPasswordView)

app_name = 'accounts'

# TODO:implement these views
# auth/ password_change/[name='password_change']
# auth/ password_change/done/ [name='password_change_done']

urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('register/', RegistrationView.as_view(), name='register'),
    path('check/', CheckIfAuthenticated.as_view(), name='check'),
    path('verify/<uidb64>/<token>/', EmailVerificationView.as_view(),
         name='email_verification'),
    path('reset/', ResetPasswordView.as_view(), name='password_reset'),
    path('reset/confirm/', PasswordResetConfirmView.as_view(),
         name='password_reset_confirm')
]
