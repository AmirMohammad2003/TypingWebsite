"""accounts.urls
url routings for the account application.
"""

from django.urls import path, include

from .views import (CheckIfAuthenticated, EmailVerificationView,
                    FetchUserInformation, LoginView, LogoutView,
                    PasswordChangeView, PasswordResetConfirmView,
                    RegistrationView, ResendVerificationEmail,
                    ResetPasswordView, EmailConfirmView)

urlpatterns = [
    path('reset/', ResetPasswordView.as_view(), name='password_reset'),
    path('reset/confirm/', PasswordResetConfirmView.as_view(),
         name='password_reset_confirm_v1'),
    path('resend/verification/', ResendVerificationEmail.as_view(),
         name='resend_verification'),
    path('v2/', include('dj_rest_auth.urls')),
    path('v2/registration/account-confirm-email/<str:key>/', EmailConfirmView.as_view(), name='confirm_email'),
    path('v2/registration/', include('dj_rest_auth.registration.urls')),
]
