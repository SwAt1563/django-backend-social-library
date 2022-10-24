from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import EmailTokenObtainSerializer, RegistrationSerializer, UsernameTokenObtainSerializer
from rest_framework.generics import CreateAPIView
from rest_framework.permissions import AllowAny
from account.models import UserAccount
from rest_framework.decorators import api_view, permission_classes
from rest_framework import status
from rest_framework.response import Response
from .permissions import AdminUserPermission
from rest_framework.authtoken.models import Token
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
import jwt
from django.conf import settings
from rest_framework_simplejwt.views import TokenRefreshView
from .tasks import create_email
from .models import UserAccount

class EmailTokenObtainPairView(TokenObtainPairView):
    serializer_class = EmailTokenObtainSerializer


# just for admins
class UsernameTokenObtainPairView(TokenObtainPairView):
    serializer_class = UsernameTokenObtainSerializer
    permission_classes = (AdminUserPermission,)


class RegisterUserAPIView(CreateAPIView):
    permission_classes = (AllowAny,)
    serializer_class = RegistrationSerializer

    def post(self, request, *args, **kwargs):
        response = super(RegisterUserAPIView, self).post(request, *args, **kwargs)
        if response.status_code == 201:
            data = response.data
            create_email.delay(
                user_username=data['username'],  # user username - this must be added
                email_account="do not reply",  # the email account being used
                subject='Thanks for signing up',
                email=data['email'],  # who to email
                cc=[],
                template="account/hello.html",  # template to be used
            )
        return response


# will generate token that will delete after 1h
@api_view(['POST'])
@permission_classes((AllowAny,))
def check_email_and_answer(request):
    if request.method == 'POST':
        data = request.data
        email = data.get('email', '')
        question = data.get('question', '')
        answer = data.get('answer', '')
        try:
            user = UserAccount.objects.get(email=email, question=question, answer=answer)

        except UserAccount.DoesNotExist:
            return Response({'error': 'Wrong inputs'}, status=status.HTTP_204_NO_CONTENT)

        token, created = Token.objects.get_or_create(user=user)

        response = {'reset_password_token': token.key}
        return Response(response, status=status.HTTP_200_OK)
    return Response(status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes((AllowAny,))
def change_password(request):
    if request.method == 'POST':
        data = request.data

        try:
            new_password = data.get('new_password', '')
            validate_password(new_password)
        except ValidationError:
            return Response({'error': 'not valid password'}, status=status.HTTP_400_BAD_REQUEST)

        reset_password_token = data.get('reset_password_token', '')

        try:
            token = Token.objects.get(key=reset_password_token)
        except Token.DoesNotExist:
            return Response({'error': 'reset_password_token not exist'}, status=status.HTTP_400_BAD_REQUEST)

        user = token.user

        user.set_password(new_password)
        user.save()

        token.delete()

        return Response(status=status.HTTP_200_OK)
    return Response(status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes((AllowAny,))
def check_token_expired(request):
    if request.method == 'POST':
        try:

            activation_token = request.data['access']
            payload = jwt.decode(activation_token, settings.SECRET_KEY, algorithms=['HS256'])

            return Response({'access': activation_token}, status=status.HTTP_200_OK)
        except jwt.ExpiredSignatureError as identifier:

            # payload = jwt.decode(request.GET['activation_token'], settings.SECRET_KEY, algorithms=['HS256'],
            #                      options={"verify_signature": False})

            # we send the refresh token by request
            response = TokenRefreshView.as_view()(request=request._request)

            if response.status_code == 200:
                return Response({'access': response.data['access']}, status=status.HTTP_200_OK)

            return Response(status=status.HTTP_403_FORBIDDEN)
    return Response(status=status.HTTP_400_BAD_REQUEST)
