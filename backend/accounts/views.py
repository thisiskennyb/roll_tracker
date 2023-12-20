# views.py
from rest_framework.generics import CreateAPIView
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from .serializers import SignupSerializer
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from django.core.exceptions import ValidationError
from rest_framework import serializers
from django.core.mail import send_mail
from django.core.mail import EmailMessage



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
        # serializer.save()
        created_object = serializer.save()
        to_email = 'kendbonnette@gmail.com'
        email = EmailMessage("howdy Ken", "I hope you get this", to=[to_email])
        email.send()
        # send_mail('Subject here','Here is the message.','kendbonnette@gmail.com', 
        #     [created_object.email],  fail_silently=False,)
        

    #         current_site = get_current_site(request)
    #         mail_subject = 'Activate your blog account.'
    #         message = render_to_string('acc_active_email.html', {
    #             'user': user,
    #             'domain': current_site.domain,
    #             'uid':urlsafe_base64_encode(force_bytes(user.pk)),
    #             'token':account_activation_token.make_token(user),
    #         })
            # to_email = form.cleaned_data.get('email')
            # email = EmailMessage(
            #             mail_subject, message, to=[to_email]
            # )
    #         email.send()
    #         return HttpResponse('Please confirm your email address to complete the registration')
    # else:
    #     form = SignupForm()
    # return render(request, 'signup.html', {'form': form})






        # Return a success response
        return Response({'message': 'User created successfully'}, status=status.HTTP_201_CREATED)
