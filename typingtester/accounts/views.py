"""accounts.views
Endpoints for user authentication and authorization.
"""
from django.conf import settings
from django.contrib.auth import (authenticate, get_user_model, login, logout,
                                 update_session_auth_hash)
from django.contrib.auth.tokens import default_token_generator
from django.http import JsonResponse
from django.shortcuts import redirect
from django.utils.decorators import method_decorator
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.views import View
from django.views.decorators.csrf import csrf_exempt, ensure_csrf_cookie
from django.views.decorators.debug import sensitive_post_parameters

from .forms import (PasswordResetConfirmForm, PasswordResetEmailSubmissionForm,
                    UserRegistrationForm, PasswordChangeForm)
from .mail import send_email_verification_mail, send_reset_password_mail


class APILoginRequiredMixin:  # pylint: disable=too-few-public-methods
    """
    APILoginRequiredMixin
    Mixin for API views that require a user to be logged in.
    """

    not_logged_in_message = 'You must be logged in to access this page.'

    def dispatch(self, request, *args, **kwargs):
        """
        checks if the user is logged in and returns an error if not.
        """
        if not request.user.is_authenticated:
            return JsonResponse(
                {'success': 'false', 'message': self.not_logged_in_message},
                status=401  # unauthorized
            )

        return super().dispatch(request, *args, **kwargs)


class LoginView(View):
    """LoginView
    endpoint for user login.
    csrf_cookie is required.
    only accepts POST requests.
    """

    @method_decorator(sensitive_post_parameters())
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    @method_decorator(ensure_csrf_cookie)
    def post(self, request, *args, **kwargs):  # pylint: disable=unused-argument, no-self-use
        """
        POST request handler.
        receives username, password and remember_me from request.
        :param request: request object
        :return JsonResponse with success or failure status
        if the request is successful, the username are returned.
        and session is set.
        """
        if request.user.is_authenticated:
            return JsonResponse({'success': 'true', 'username': request.user.username})

        # I am going to change how this works in the future.
        username = request.POST.get('username')
        password = request.POST.get('password')

        remember_me = request.POST.get('remember_me', None)

        user = authenticate(username=username, password=password)
        if user is not None:
            if not user.is_active:
                return JsonResponse({
                    'success': 'false', 'message': 'Invalid username or password.'
                })

            if not user.is_email_verified and not user.is_superuser:
                return JsonResponse({
                    'success': 'false', 'message': 'Please verify your email address.'
                })

            if remember_me is None:
                request.session.set_expiry(0)

            login(request, user)
            return JsonResponse({'success': 'true', 'username': username})

        return JsonResponse(
            {'success': 'false', 'message': 'Invalid username or password'}
        )


class RegistrationView(View):
    """RegistrationView
    endpoint for user registration.
    csrf_cookie is required.
    only accepts POST requests.
    """

    @method_decorator(sensitive_post_parameters())
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    @method_decorator(ensure_csrf_cookie)
    def post(self, request, *args, **kwargs):  # pylint: disable=unused-argument, no-self-use
        """
        POST request handler.
        receives username, password1, password2 and email from request.
        :param request: request object
        :return JsonResponse with success or failure status
        if the request is successful, email verification mail is sent.
        if the user is logged in, the username is returned.
        """
        if request.user.is_authenticated:
            return JsonResponse({'success': 'true', 'username': request.user.username})

        form = UserRegistrationForm(request.POST)

        if form.is_valid():
            user = form.save()
            # TODO resend button  # pylint: disable=fixme
            if send_email_verification_mail(request, user):
                if not request.session.session_key:
                    request.session.create()

                request.session['_id'] = urlsafe_base64_encode(
                    str(user.id).encode()
                )
                return JsonResponse({
                    'success': 'unknown',
                    'message': "Please check your inbox to verify your email address"
                })

            return JsonResponse({
                'success': 'unknown',
                'message': "Internal Server Error"
            })

        errors = []
        for key, value in form.errors.items():
            errors += [key + ": " + value[0]]
        return JsonResponse({'success': 'false', 'errors': errors})


class LogoutView(View):
    """LogoutView
    endpoint for user logout.
    csrf_cookie is required.
    only accepts POST requests.
    """

    @method_decorator(ensure_csrf_cookie)
    def post(self, request, *args, **kwargs):  # pylint: disable=unused-argument, no-self-use
        """
        POST request handler.
        :param request: request object
        :return JsonResponse with success or failure status
        if the request is successful, the user is logged out.
        """
        if request.user.is_authenticated:
            logout(request)
            return JsonResponse({'success': 'true'})

        return JsonResponse({'success': 'false'})


class CheckIfAuthenticated(View):
    """CheckIfAuthenticated
    endpoint for checking if user is authenticated.
    csrf_cookie is required.
    only accepts POST requests.
    """

    @method_decorator(ensure_csrf_cookie)
    def post(self, request, *args, **kwargs):  # pylint: disable=unused-argument, no-self-use
        """
        POST request handler.
        :param request: request object
        :return JsonResponse with success or failure status
        if the request is successful, the username is returned.
        """
        if request.user.is_authenticated:
            return JsonResponse({'Authenticated': 'true', 'username': request.user.username})

        return JsonResponse({'Authenticated': 'false'})


class EmailVerificationView(View):
    """EmailVerificationView
    endpoint for verifying email address.
    only accepts GET requests.
    """

    @method_decorator(sensitive_post_parameters())
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    @method_decorator(csrf_exempt)
    def get(self, request, uidb64, token, *args, **kwargs):  # pylint: disable=unused-argument, no-self-use
        """
        GET request handler.
        :param request: request object
        :param uidb64: base64 encoded user id
        :param token: token generated by default_token_generator
        :return JsonResponse with success or failure status
        if the request is successful, the user is redirected to success page.
        """
        primary_key = urlsafe_base64_decode(uidb64)
        user_model = get_user_model()
        if not primary_key.isdigit():
            return JsonResponse({'success': 'false', 'message': "Access Denied"})

        user = user_model.objects.filter(pk=primary_key)
        if user.exists():
            user = user[0]
            if default_token_generator.check_token(user, token):
                if user.is_email_verified is False:
                    user.is_email_verified = True
                    user.save()

                return redirect(settings.FRONTEND + '/success/emailVerified')

        return JsonResponse({'success': 'false', 'message': "Access Denied"})


class ResetPasswordView(View):
    """ResetPasswordView
    endpoint for resetting password.
    csrf_cookie is required.
    only accepts POST requests.
    """

    @method_decorator(ensure_csrf_cookie)
    def post(self, request, *args, **kwargs):  # pylint: disable=unused-argument, no-self-use
        """
        POST request handler.
        receives email from request.
        :param request: request object
        :return JsonResponse with success or failure status
        if the request is successful, password reset mail is sent.
        """
        if request.user.is_authenticated:
            return JsonResponse({
                'success': 'false', 'message': 'You are already logged in.'
            })

        form = PasswordResetEmailSubmissionForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            user_model = get_user_model()
            user_result = user_model.objects.filter(email=email)
            if user_result.exists():
                user = user_result[0]
                if user.is_active:
                    if user.is_email_verified:
                        send_reset_password_mail(user, email)
                        user.set_unusable_password()
                        return JsonResponse({
                            'success': 'true', "message": "An email was sent to your inbox."
                        })

                    # TODO resend button # pylint: disable=fixme
                    send_email_verification_mail(request, user)
                    return JsonResponse({
                        'success': 'true',
                        "message": "pls verify your email address first then \
                                    try again(the email was sent to your inbox)."
                    })

            # TODO resend button # pylint: disable=fixme
            # Just for tricking bad guys
            return JsonResponse({'success': 'true', "message": "An email was sent to your inbox."})

        errors = []
        for key, value in form.errors.items():
            errors += [key + ": " + value[0]]

        return JsonResponse({'success': 'false', 'errors': errors})


class PasswordResetConfirmView(View):
    """PasswordResetConfirmView
    endpoint for confirming password reset
    and making a new password.
    csrf_cookie is required.
    only accepts POST requests.
    """

    @method_decorator(sensitive_post_parameters())
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    @method_decorator(ensure_csrf_cookie)
    def post(self, request, *args, **kwargs):  # pylint: disable=unused-argument, no-self-use
        """
        POST request handler.
        receives password1 and password2 from request.
        :param request: request object
        :return JsonResponse with success or failure status
        if the request is successful, password is reset.
        then the user is redirected to success page.
        """
        form = PasswordResetConfirmForm(request.POST)
        if form.is_valid():
            form.save()
            return JsonResponse({
                'success': 'true', 'location': '/success/passwordResetDone'
            })

        errors = []
        for key, value in form.errors.items():
            errors += [key + ": " + value[0]]
        return JsonResponse({'success': 'false', 'errors': errors})


class FetchUserInformation(APILoginRequiredMixin, View):
    """FetchUserInformation
    endpoint for fetching user information.
    csrf_cookie is required.
    only accepts POST requests.
    """

    @method_decorator(ensure_csrf_cookie)
    def post(self, request, *args, **kwargs):  # pylint: disable=unused-argument, no-self-use
        """
        POST request handler.
        receives email from request.
        :param request: request object
        :return JsonResponse with success or failure status and user information
        if the request is successful, user information is returned.
        """

        # if the user is logged in so the account is active and verified
        # so we don't need to check for that.
        # but i am doing that here for the sake of security.
        if request.user.is_email_verified:
            return JsonResponse({
                'success': 'true',
                'username': request.user.username,
                'email': request.user.email
            })

        return JsonResponse({'success': 'false', 'message': "Access Denied"}, status=403)


class PasswordChangeView(APILoginRequiredMixin, View):
    """PasswordChangeView
    endpoint for changing password.
    csrf_cookie is required.
    only accepts POST requests.
    """

    @method_decorator(sensitive_post_parameters())
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    @method_decorator(ensure_csrf_cookie)
    def post(self, request, *args, **kwargs):  # pylint: disable=unused-argument, no-self-use
        """
        POST request handler.
        receives password1 and password2 from request.
        :param request: request object
        :return JsonResponse with success or failure status
        if the request is successful, password is changed.
        """

        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            form.save()
            update_session_auth_hash(request, request.user)
            return JsonResponse({'success': 'true'})

        errors = []
        for key, value in form.errors.items():
            errors += [key + ": " + value[0]]

        return JsonResponse({'success': 'false', 'errors': errors})


# not protected against click spamming because it's not a massive website.
# I probably will add rate limiting in the future.
class ResendVerificationEmail(View):
    """ResendVerificationEmail
    endpoint for resending verification email.
    csrf_cookie is required.
    only accepts POST requests.
    """

    @method_decorator(ensure_csrf_cookie)
    def post(self, request, *args, **kwargs):  # pylint: disable=unused-argument, no-self-use
        """
        POST request handler.
        receives email from request.
        :param request: request object
        :return JsonResponse with success or failure status
        if the request is successful, verification email is sent.
        """

        if request.user.is_authenticated:
            return JsonResponse({
                'success': 'false', 'message': 'You are already logged in.'
            })

        if request.session.get('_id', None) is None:
            return JsonResponse({
                'success': 'false', 'message': 'Access Denied.'
            })

        _id = urlsafe_base64_decode(request.session.get('_id'))
        user_model = get_user_model()
        user_result = user_model.objects.filter(id=_id)
        if user_result.exists():
            user = user_result[0]
            if user.is_active:
                if user.is_email_verified:
                    return JsonResponse({
                        'success': 'false', 'message': 'You are already verified.'
                    })

                send_email_verification_mail(request, user)
                return JsonResponse({
                    'success': 'true', "message": "Verification email was sent to your inbox."
                })

        return JsonResponse({'success': 'false', 'message': "Access Denied."})
