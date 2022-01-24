from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import ensure_csrf_cookie

from .forms import UserRegistrationForm


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
            if remember_me is None:
                request.session.set_expiry(0)

            login(request, user)
            return JsonResponse({'success': 'true', 'username': username})

        else:
            return JsonResponse({'success': 'false', 'message': 'Invalid username or password'})


class RegistrationView(View):

    @method_decorator(ensure_csrf_cookie)
    def post(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return JsonResponse({'success': 'true', 'username': request.user.username})

        form = UserRegistrationForm(request.POST)

        if form.is_valid():
            user = form.save()
            login(request, user)

            return JsonResponse({'success': 'true', 'username': user.username})

        else:
            return JsonResponse({'success': 'false', 'errors': form.errors})


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
