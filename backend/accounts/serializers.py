from rest_framework.serializers import ModelSerializer
from django.contrib.auth.models import User
from rest_framework import serializers
from django.core.validators import EmailValidator

class SignupSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(write_only=True, validators=[EmailValidator()])

    class Meta:
        model = User
        fields = ['username', 'password', 'email']