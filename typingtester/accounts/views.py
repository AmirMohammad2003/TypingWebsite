from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import ensure_csrf_cookie, csrf_exempt
from django.utils.http import urlsafe_base64_decode
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth import get_user_model
from django.shortcuts import redirect
from django.conf import settings
from django.contrib.messages import constants
from django.contrib import messages

from .forms import UserRegistrationForm
from .mail import send_email_verification_mail


class LoginView(View):

    @method_decorator(ensure_csrf_cookie)
    def post(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return JsonResponse({'success': 'true', 'username': request.user.username})

        username = request.POST.get('username')
        password = request.POST.get('password')

        remember_me = request.POST.get('remember_me', None)

        user = authenticate(username=username, password=password)
        if user is not None:
            if not user.is_active:
                return JsonResponse(
                    {'success': 'false', 'message': 'Invalid username or password.'}
                )

            if not user.is_email_verified and not user.is_superuser:
                return JsonResponse(
                    {'success': 'false', 'message': 'Please verify your email address.'}
                )

            if remember_me is None:
                request.session.set_expiry(0)

            login(request, user)
            return JsonResponse({'success': 'true', 'username': username})

        else:
            return JsonResponse(
                {'success': 'false', 'message': 'Invalid username or password'}
            )


class RegistrationView(View):

    @method_decorator(ensure_csrf_cookie)
    def post(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return JsonResponse({'success': 'true', 'username': request.user.username})

        form = UserRegistrationForm(request.POST)

        if form.is_valid():
            user = form.save()
            # request.session.set_expiry(0)
            # login(request, user)
            if (send_email_verification_mail(request, user)):
                return JsonResponse(
                    {
                        'success': 'unknown',
                        'message': "Please check your inbox to verify your email address"
                    }
                )

            else:
                return JsonResponse(
                    {
                        'success': 'unknown',
                        'message': "Internal Server Error"
                    }
                )

        else:
            errors = []
            for k, v in form.errors.items():
                errors += v
            return JsonResponse({'success': 'false', 'errors': errors})


class LogoutView(View, LoginRequiredMixin):

    @method_decorator(ensure_csrf_cookie)
    def post(self, request, *args, **kwargs):
        logout(request)
        return JsonResponse({'success': 'true'})


class CheckIfAuthenticated(View):

    @method_decorator(ensure_csrf_cookie)
    def post(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return JsonResponse({'Authenticated': 'true', 'username': request.user.username})

        return JsonResponse({'Authenticated': 'false'})


class PasswordVerificationView(View):

    @method_decorator(csrf_exempt)
    def get(self, request, uidb64, token, *args, **kwargs):
        pk = urlsafe_base64_decode(uidb64)
        User = get_user_model()
        user = User.objects.filter(pk=pk)
        if user.exists():
            user = user[0]
            if (default_token_generator.check_token(user, token)):
                if user.is_email_verified == False:
                    user.is_email_verified = True
                    user.save()

                return redirect(settings.FRONTEND + '/success/emailVerified')

        return JsonResponse({'success': 'false', 'message': "Access Denied"}, status=403)
