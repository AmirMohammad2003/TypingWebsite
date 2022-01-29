"""accounts.forms
Forms used for the accounts application
like the registration form and the login form.
"""

from django import forms
from django.contrib.auth import get_user_model, password_validation
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.tokens import default_token_generator
from django.core import validators
from django.core.exceptions import ValidationError
from django.utils.http import urlsafe_base64_decode


user_model = get_user_model()


class UserRegistrationForm(UserCreationForm):
    """
    Form for registering a new user.
    inherits from UserCreationForm
    and adds the email field to the form.
    """
    email = forms.EmailField(validators=[validators.EmailValidator])

    class Meta:  # pylint: disable=too-few-public-methods
        """Meta class for UserRegistrationForm"""
        model = user_model
        fields = ('email', 'username', 'password1', 'password2')


class PasswordResetEmailSubmissionForm(forms.Form):
    """Password reset email submission form
    used for getting password reset emails.
    """
    email = forms.EmailField(validators=[validators.EmailValidator])


class PasswordResetConfirmForm(forms.Form):
    """Password reset confirmation form
    used for confirming the password reset.
    and setting the new password.
    """

    error_messages = {
        'password_mismatch': 'The two password fields didn\'t match.',
        'invalid_token': 'The token is either invalid or Corrupted',
    }
    uidb64 = forms.CharField(required=True)
    token = forms.CharField(required=True)
    password1 = forms.CharField(strip=False, required=True)
    password2 = forms.CharField(strip=False, required=True)

    def clean_password2(self):
        """
        checks if the two passwords match.
        and raises an error if they don't.
        and if the passwords are not blank strings.
        """
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise ValidationError(
                self.error_messages['password_mismatch'],
                code='password_mismatch',
            )
        password_validation.validate_password(password2)
        return password2

    def clean_uidb64(self):
        """
        decodes uidb64 to the user id.
        checks if the id is valid.
        and returns the user id.
        """
        try:
            primary_key = urlsafe_base64_decode(
                self.cleaned_data.get('uidb64')
            )

        except Exception as error:
            raise ValidationError(
                self.error_messages['invalid_token'],
                code='invalid_token'
            ) from error

        if not primary_key.isdigit():
            raise ValidationError(
                self.error_messages['invalid_token'],
                code='invalid_token'
            )

        return primary_key

    def clean_token(self):
        """
        checks if the token is valid.
        and returns the user if it is valid.
        """
        primary_key = self.cleaned_data.get('uidb64')
        user_result = user_model.objects.filter(pk=primary_key)
        if not user_result.exists():
            raise ValidationError(
                f'user doesn\'t exist {primary_key}',
                code='invalid_token'
            )

        user = user_result[0]
        if default_token_generator.check_token(user, self.cleaned_data.get('token')):
            return user

        raise ValidationError(
            self.error_messages['invalid_token'],
            code='invalid_token'
        )

    def save(self, commit=True):
        """
        saves the new password in the user object.
        and in the database if commit is True.
        """
        user = self.cleaned_data.get('token')  # it actually returns the user
        password = self.cleaned_data.get('password2')

        # probably should check if user has usable password or not.
        user.set_password(password)

        if commit:
            user.save()

        return user
