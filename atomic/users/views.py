import jwt
from datetime import UTC, datetime, timedelta

from django.db.models import Q
from django.core.exceptions import ObjectDoesNotExist
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.response import Response

from companies.models import Company
from companies.modules import create_company_from_request
from .models import User
from .serializers import UserSerializer
from atomic.modules import get_user_from_jwt_token


class RegisterView(APIView):
    def post(self, request):
        try:
            user = User.objects.get(Q(email=request.data.get('email')) | Q(username=request.data.get('username')))
            return Response({'detail': f'{user.first_name}, ya tienes una cuenta creada ¡Inicia Sesión!'},
                            status=status.HTTP_400_BAD_REQUEST)
        except ObjectDoesNotExist:
            pass

        company_uuid = request.data.get('company_uuid')
        if company_uuid == 'New':
            company_serialized, payload = create_company_from_request(request)
            if payload:
                return Response(company_serialized, status=payload)
            company_uuid = company_serialized['uuid']

        user_data = request.data.copy()
        user_data['company'] = company_uuid
        serializer = UserSerializer(data=user_data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'User created successfully'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    def post(self, request):
        email_username = request.data.get('email-username')
        password = request.data['password']

        if not email_username:
            return Response({'detail': 'Debes ingresar email o usuario'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            user = User.objects.get(Q(email=email_username) | Q(username=email_username))
        except ObjectDoesNotExist:
            return Response({'detail': 'Aún no tenemos tu cuenta registrada en nuestro sistema'}, status=status.HTTP_404_NOT_FOUND)

        if not user.check_password(password):
            return Response({'detail': 'Oops... Contraseña incorrecta'}, status=status.HTTP_400_BAD_REQUEST)

        payload = {
            'uuid': str(user.uuid),
            'exp': datetime.now(UTC) + timedelta(minutes=90),
            'iat': datetime.now(UTC)
        }

        token = jwt.encode(payload, 'secret', algorithm='HS256')

        response = Response()
        response.set_cookie(key='jwt', value=token, httponly=True)

        user_serializer = UserSerializer(user)

        response.data = {
            'user': user_serializer.data,
            'token': token,
            'jwt': token
        }

        return response


class LogoutView(APIView):
    def post(self, request):
        response = Response()
        response.delete_cookie('jwt')
        response.data = {
            'message': 'success'
        }
        return response


class ChangePasswordView(APIView):
    def post(self, request):
        token = request.COOKIES.get('jwt')
        user = get_user_from_jwt_token(token)

        old_password = request.data['old_password']
        new_password = request.data['new_password']

        if not user.check_password(old_password):
            return Response({'detail': 'Invalid password'}, status=status.HTTP_400_BAD_REQUEST)

        user.set_password(new_password)
        user.save()

        return Response({'message': 'success'}, status=status.HTTP_200_OK)


class UserView(APIView):
    def get(self, request):
        token = request.COOKIES.get('jwt')
        user = get_user_from_jwt_token(token)
        serializer = UserSerializer(user)

        response = Response()
        response.data = {
            'user': serializer.data,
            'token': token
        }

        return response

    def put(self, request):
        token = request.COOKIES.get('jwt')
        user = get_user_from_jwt_token(token)
        serializer = UserSerializer(user, data=request.data, partial=True)

        serializer.is_valid(raise_exception=True)
        serializer.save()

        response = Response()
        response.data = {
            'user': serializer.data,
            'token': token
        }

        return response
