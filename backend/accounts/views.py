from rest_framework.generics import CreateAPIView
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from .serializers import SignupSerializer
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from django.core.exceptions import ValidationError
from rest_framework import serializers
from django.core.mail import EmailMessage   
from .tokens import email_verification_token


from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes
# from django.utils.encoding import force_text
from django.utils.http import urlsafe_base64_encode
from django.utils.http import urlsafe_base64_decode
from django.template.loader import render_to_string

from django.shortcuts import render

class SignupView(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = SignupSerializer
    permission_classes = [AllowAny]

    def perform_create(self, serializer):
        # Extract username, password, and email from serializer
        username = serializer.validated_data["username"]
        password = serializer.validated_data["password"]
        email = serializer.validated_data["email"]

        # Validate the password using Django's password validators
        try:
            validate_password(password, user=User)
        except ValidationError as e:
            # Raise a serializers.ValidationError to trigger a 400 Bad Request response
            raise serializers.ValidationError(detail=e.messages)

        # Create the user if the password is valid
        user = User.objects.create_user(username=username, email=email, password=password)
        serializer.instance = user
        serializer.validated_data['user'] = user
        serializer.validated_data['user_id'] = user.id
        user.is_active = False
        user.save()

        self._send_email_verification(user)

        return Response({'message': 'User created successfully'}, status=status.HTTP_201_CREATED)


    def _send_email_verification(self, user):
        print(user.email.rstrip(),"this right here")
        current_site = get_current_site(self.request)
        subject = 'Activate Your Account'
        body = render_to_string(
            'email_verification.html',
            {
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': email_verification_token.make_token(user),
            }
        )
        EmailMessage(to=[user.email], subject=subject, body=body).send()