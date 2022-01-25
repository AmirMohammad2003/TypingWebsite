from django.urls import path  # , include

from .views import (CheckIfAuthenticated, LoginView, LogoutView,
                    PasswordVerificationView, RegistrationView)

app_name = 'accounts'

# TODO:implement these views
# auth/ password_change/done/ [name='password_change_done']
# auth/ password_reset/ [name='password_reset']
# auth/ password_reset/done/ [name='password_reset_done']
# auth/ reset/<uidb64>/<token>/ [name='password_reset_confirm']
# auth/ reset/done/ [name='password_reset_complete']

urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('register/', RegistrationView.as_view(), name='register'),
    path('check/', CheckIfAuthenticated.as_view(), name='check'),
    path('verify/<uidb64>/<token>/', PasswordVerificationView.as_view(),
         name='password_verification')
    # path('reset/', ResetAuthenticated.as_view(), name='reset')
]
