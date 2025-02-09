from rest_framework import serializers
from django.contrib.auth import authenticate
from django.contrib.auth.password_validation import validate_password
from django.utils.translation import gettext_lazy as _
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from .models import CustomUser

class UserSerializer(serializers.ModelSerializer):
    # Return full name from first_name and last_name
    name = serializers.SerializerMethodField()

    class Meta:
        model = CustomUser
        fields = ('id', 'email', 'name', 'is_staff', 'is_agent', 'role')
        read_only_fields = ('is_staff', 'is_agent', 'role')

    def get_name(self, obj):
        return obj.full_name  # Uses the property defined in the model


class RegisterSerializer(serializers.ModelSerializer):
    # Accept a full name from the client for input only.
    name = serializers.CharField(required=True, write_only=True)
    password = serializers.CharField(
        write_only=True,
        required=True,
        validators=[validate_password]
    )
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = CustomUser
        # The client provides a "name", which will be split into first and last names.
        fields = ('email', 'password', 'password2', 'name')

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({
                "password": _("Password fields didn't match.")
            })
        return attrs

    def create(self, validated_data):
        # Extract the full name from the incoming data.
        name = validated_data.pop('name', '')
        # Split the full name into first_name and last_name.
        names = name.split(' ', 1)
        validated_data['first_name'] = names[0]
        validated_data['last_name'] = names[1] if len(names) > 1 else ''
        # Remove password2 since it's not needed.
        validated_data.pop('password2', None)
        user = CustomUser.objects.create_user(**validated_data)
        return user

    def to_representation(self, instance):
        """
        Override the default representation so that the response
        uses the UserSerializer, which provides the computed full name.
        """
        return UserSerializer(instance, context=self.context).data


class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    def validate(self, attrs):
        data = super().validate(attrs)
        data['user'] = UserSerializer(self.user).data
        return data

    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['email'] = user.email
        token['is_staff'] = user.is_staff
        token['is_agent'] = user.is_agent
        return token


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(
        style={'input_type': 'password', 'trim_whitespace': False}
    )

    def validate(self, data):
        email = data.get('email')
        password = data.get('password')

        if email and password:
            user = authenticate(
                request=self.context.get('request'),
                email=email,
                password=password
            )

            if not user:
                msg = _('Unable to log in with provided credentials.')
                raise serializers.ValidationError(msg, code='authorization')

            if not user.is_active:
                msg = _('User account is disabled.')
                raise serializers.ValidationError(msg, code='authorization')
        else:
            msg = _('Must include "email" and "password".')
            raise serializers.ValidationError(msg, code='authorization')

        data['user'] = user
        return data
