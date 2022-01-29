from calendar import c
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth import get_user_model
from django.core import validators
from django.core.exceptions import ValidationError
from django.contrib.auth import password_validation
from django.utils.http import urlsafe_base64_decode
from django.contrib.auth.tokens import default_token_generator


def validate_equal_to(value1, value2):
    if value1 != value2:
        raise ValidationError()


UserModel = get_user_model()


class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField(validators=[validators.EmailValidator])

    class Meta:
        model = UserModel
        fields = ('email', 'username', 'password1', 'password2')


class PasswordResetEmailSubmissionForm(forms.Form):
    email = forms.EmailField(validators=[validators.EmailValidator])


class PasswordResetConfirmForm(forms.Form):
    error_messages = {
        'password_mismatch': 'The two password fields didn\'t match.',
        'invalid_token': 'The token is either invalid or Corrupted',
    }
    uidb64 = forms.CharField(required=True)
    token = forms.CharField(required=True)
    password1 = forms.CharField(strip=False, required=True)
    password2 = forms.CharField(strip=False, required=True)

    def clean_password2(self):
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
        try:
            pk = urlsafe_base64_decode(self.cleaned_data.get('uidb64'))

        except:
            raise ValidationError(
                self.error_messages['invalid_token'],
                code='invalid_token'
            )

        if not pk.isdigit():
            raise ValidationError(
                self.error_messages['invalid_token'],
                code='invalid_token'
            )

        return pk

    def clean_token(self):
        pk = self.cleaned_data.get('uidb64')
        user_result = UserModel.objects.filter(pk=pk)
        if not user_result.exists():
            raise ValidationError(
                'user doesn\'t exist {}'.format(pk),
                code='invalid_token'
            )

        user = user_result[0]
        if (default_token_generator.check_token(user, self.cleaned_data.get('token'))):
            return user

        else:
            raise ValidationError(
                self.error_messages['invalid_token'],
                code='invalid_token'
            )

    def save(self, commit=True):
        user = self.cleaned_data.get('token')  # it actually returns the user
        password = self.cleaned_data.get('password2')

        # probably should check if user has usable password or not.
        user.set_password(password)

        if commit:
            user.save()

        return user
