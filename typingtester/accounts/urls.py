"""accounts.urls
url routings for the account application.
"""

from django.urls import path

from .views import (CheckIfAuthenticated, EmailVerificationView,
                    FetchUserInformation, LoginView, LogoutView,
                    PasswordChangeView, PasswordResetConfirmView,
                    RegistrationView, ResendVerificationEmail,
                    ResetPasswordView)

app_name = 'accounts'  # pylint: disable=invalid-name

urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('register/', RegistrationView.as_view(), name='register'),
    path('check/', CheckIfAuthenticated.as_view(), name='check'),
    path('verify/<uidb64>/<token>/', EmailVerificationView.as_view(),
         name='email_verification'),
    path('reset/', ResetPasswordView.as_view(), name='password_reset'),
    path('reset/confirm/', PasswordResetConfirmView.as_view(),
         name='password_reset_confirm'),
    path('user/info/', FetchUserInformation.as_view(), name='fetch_user_info'),
    path('password/change/', PasswordChangeView.as_view(),
         name='password_change'),
    path('resend/verification/', ResendVerificationEmail.as_view(),
         name='resend_verification'),
]
