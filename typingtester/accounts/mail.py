"""accounts.mail
Mail related functions
"""

from smtplib import SMTPException
from urllib.parse import urlunparse

from django.conf import settings
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
# if "mailer" in settings.INSTALLED_APPS:
# from mailer import send_mail
# else:
from django.core.mail import send_mail
from django.utils.http import urlsafe_base64_encode


def send_simple_mail(subject, message, _from, _to):
    """Send simple mail.
    :param subject: Subject of the mail
    :param message: Message of the mail
    :param _from: From email
    :param _to: To email
    """
    try:
        send_mail(
            subject=subject,
            message=message,
            from_email=_from,
            recipient_list=[_to],
            fail_silently=False,
        )

    except SMTPException:
        return False

    else:
        return True


def send_email_verification_mail(request, user):
    """Send email verification email to user.
    :param request: request object
    :param user: user object
    """
    token = default_token_generator.make_token(user)
    uid = urlsafe_base64_encode(str(user.id).encode())
    base = get_current_site(request)

    url = urlunparse(
        (
            "http",
            str(base),
            "auth/verify/" + str(uid) + "/" + str(token) + "/",
            '',
            '',
            '',
        )
    )

    return send_simple_mail(
        "Verify Your Email",  # Subject
        f"Please Click on this link to verify your email\n{url}",  # Message
        settings.EMAIL_HOST_USER,  # FromEmail
        user.email  # ToEmail
    )


def send_reset_password_mail(user, email):
    """Send reset password email to user.
    :param user: user object
    :param email: user email
    """
    # i had a better idea to implement password reset but this is how i ended up doing it.
    token = default_token_generator.make_token(user)
    uid = urlsafe_base64_encode(str(user.id).encode())

    url = settings.FRONTEND + "/account/reset/" + \
        str(uid) + "/" + str(token) + "/"

    return send_simple_mail(
        "Reset Your Password",  # Subject

        # Message
        f"Please Click on this link to proceed reseting your password\n{url}",

        settings.EMAIL_HOST_USER,  # FromEmail
        email  # ToEmail
    )
