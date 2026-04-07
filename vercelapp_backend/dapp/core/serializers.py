# core/serializers.py

from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from rest_framework.validators import UniqueValidator
from dj_rest_auth.serializers import PasswordResetSerializer, LoginSerializer as DefaultLoginSerializer
from dj_rest_auth.registration.serializers import RegisterSerializer as DefaultRegisterSerializer
from dj_rest_auth.serializers import PasswordChangeSerializer as DefaultPasswordChangeSerializer
from django.conf import settings
from allauth.account.forms import ResetPasswordForm
from allauth.account.adapter import get_adapter
from allauth.account.utils import user_pk_to_url_str
from django.contrib.auth.tokens import default_token_generator
User = get_user_model()

class LoginSerializer(DefaultLoginSerializer):
    email = None
    def validate(self, attrs):
        print(f"🔍 Login attempt - Username: {attrs.get('username')}, Password: {'*' * len(attrs.get('password', ''))}")
        return super().validate(attrs)

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'date_joined']
        read_only_fields = ['id', 'date_joined']

class RegisterSerializer(DefaultRegisterSerializer):
    first_name = serializers.CharField(required=True)
    last_name = serializers.CharField(required=True)

    def get_cleaned_data(self):
        data = super().get_cleaned_data()
        data['first_name'] = self.validated_data.get('first_name', '')
        data['last_name'] = self.validated_data.get('last_name', '')
        return data

    def custom_signup(self, request, user):
        user.first_name = self.validated_data.get('first_name', '')
        user.last_name = self.validated_data.get('last_name', '')
        user.save()

# *** NEW: Validates old_password before allowing change ***
class CustomPasswordChangeSerializer(DefaultPasswordChangeSerializer):
    def validate_old_password(self, value):
        user = self.context['request'].user
        if not user.check_password(value):
            raise serializers.ValidationError("Current password is incorrect.")
        return value

    def validate(self, attrs):
        # new_password1 and new_password2 must match
        if attrs.get('new_password1') != attrs.get('new_password2'):
            raise serializers.ValidationError(
                {"new_password2": "New passwords do not match."}
            )
        # new password must differ from old
        if attrs.get('old_password') == attrs.get('new_password1'):
            raise serializers.ValidationError(
                {"new_password1": "New password must be different from your current password."}
            )
        # Run Django's built-in password validators (length, common passwords, etc.)
        user = self.context['request'].user
        validate_password(attrs.get('new_password1'), user)
        return attrs

class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True, validators=[validate_password])
    new_password2 = serializers.CharField(required=True)

    def validate(self, attrs):
        if attrs['new_password'] != attrs['new_password2']:
            raise serializers.ValidationError(
                {"new_password": "Password fields didn't match."}
            )
        return attrs

class CustomPasswordResetSerializer(PasswordResetSerializer):
    def get_email_options(self):
        return {
            'extra_email_context': {
                'password_reset_url': f"{settings.FRONTEND_URL}/auth/password-reset/confirm"
            },
        }

class CustomAllAuthPasswordResetForm(ResetPasswordForm):
    def save(self, request, **kwargs):
        email = self.cleaned_data["email"]
        token_generator = kwargs.get("token_generator", default_token_generator)

        for user in self.users:
            temp_key = token_generator.make_token(user)
            uid = user_pk_to_url_str(user)

            # --- FORCE THE NEXT.JS FRONTEND URL ---
            custom_url = f"{settings.FRONTEND_URL}/auth/forgot-password/{uid}/{temp_key}"

            context = {
                "user": user,
                "password_reset_url": custom_url,
                "request": request,
            }

            get_adapter(request).send_mail(
                "account/email/password_reset_key", email, context
            )

class CustomPasswordResetSerializer(PasswordResetSerializer):
    password_reset_form_class = CustomAllAuthPasswordResetForm