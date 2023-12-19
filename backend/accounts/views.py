from rest_framework.generics import CreateAPIView
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from .serializers import SignupSerializer
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from rest_framework import serializers
from django.core.exceptions import ValidationError


class SignupView(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = SignupSerializer
    permission_classes = [AllowAny]

    def perform_create(self, serializer):
        # Extract username and password from serializer
        username = serializer.validated_data["username"]
        password = serializer.validated_data["password"]

        # Validate the password using Django's password validators
        try:
            validate_password(password, user=User)
        except ValidationError as e:
            # Raise a serializers.ValidationError to trigger a 400 Bad Request response
            raise serializers.ValidationError(detail=e.messages)

        # Create the user if the password is valid
        user = User.objects.create_user(username=username, password=password)
        serializer.instance = user
        serializer.validated_data['user'] = user
        serializer.validated_data['user_id'] = user.id
        serializer.save()

        # Return a success response
        return Response({'message': 'User created successfully'}, status=status.HTTP_201_CREATED)
