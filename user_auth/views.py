import json
from http import HTTPStatus

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
import requests
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from rest_framework import viewsets, status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from user_auth.decorators import user_not_authenticated
from user_auth.models import Profile
from user_auth.serializers import ProfileSerializer, UserSerializer
from user_auth.utils import generate_unique_username


# Create your views here.
@method_decorator(user_not_authenticated, name='dispatch')
class RegistrationView(View):
    def post(self, request, *args, **kwargs):
        import json
        data = json.loads(request.body)
        username = data.get('username')
        first_name = data.get('first_name')
        last_name = data.get('last_name')
        email = data.get('email')
        password = data.get('password')
        password_check = data.get('password_check')

        if password != password_check:
            return JsonResponse({"message": "Passwords do not match."}, status=HTTPStatus.BAD_REQUEST)
        if User.objects.filter(username=username).exists():
            return JsonResponse({"message": "Username already taken."}, status=HTTPStatus.BAD_REQUEST)
        if User.objects.filter(email=email).exists():
            return JsonResponse({"message": "Email already taken."}, status=HTTPStatus.BAD_REQUEST)

        user = User.objects.create_user(username=username,
                                        email=email,
                                        password=password,
                                        first_name=first_name,
                                        last_name=last_name)
        user.save()

        backend = 'django.contrib.auth.backends.ModelBackend'
        login(request, user, backend=backend)

        return JsonResponse({"message": f"Registration successful! Welcome, {user.username}"},
                            status=HTTPStatus.CREATED)


@method_decorator(user_not_authenticated, name='dispatch')
@method_decorator(csrf_exempt, name='dispatch')
class LoginView(View):
    def post(self, request, *args, **kwargs):
        import json
        data = json.loads(request.body)
        username = data.get('username')
        password = data.get('password')

        if not username or not password:
            return JsonResponse({"message": "Username and password are required."}, status=HTTPStatus.BAD_REQUEST)

        if not User.objects.filter(username=username).exists():
            return JsonResponse({"message": "User with this username does not exist."}, status=HTTPStatus.BAD_REQUEST)

        user = authenticate(username=username, password=password)
        if user is None:
            return JsonResponse({"message": "Invalid password."}, status=HTTPStatus.UNAUTHORIZED)

        backend = 'django.contrib.auth.backends.ModelBackend'
        login(request, user, backend=backend)
        return JsonResponse({"message": f"Welcome, {user.username}"}, status=HTTPStatus.OK)


@method_decorator(csrf_exempt, name='dispatch')
class GoogleLogin(View):
    def post(self, request, *args, **kwargs):
        data = json.loads(request.body)
        token = data.get('token')

        response = requests.get(f"https://oauth2.googleapis.com/tokeninfo?id_token={token}")
        user_info = response.json()

        if 'email' not in user_info:
            return JsonResponse({'error': 'Invalid token'}, status=400)
        email = user_info['email']
        username = user_info['email'].split('@')[0]
        if User.objects.filter(username=username).exists():
            username = generate_unique_username(username)

        first_name = user_info.get('given_name')
        last_name = user_info.get('family_name')

        user, created = User.objects.get_or_create(email=email, defaults={'username': username,
                                                                          'first_name': first_name,
                                                                          'last_name': last_name})

        backend = 'allauth.account.auth_backends.AuthenticationBackend'
        login(request, user, backend=backend)

        return JsonResponse({'message': 'User authenticated', 'created': created}, status=200)


@method_decorator(login_required, name='dispatch')
@method_decorator(csrf_exempt, name='dispatch')
class LogoutView(View):
    def post(self, request, *args, **kwargs):
        logout(request)
        return JsonResponse({"message": "Logged out successfully."}, status=HTTPStatus.OK)


class ProfileViewSet(viewsets.ModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Profile.objects.filter(user=self.request.user)

    def update(self, request, *args, **kwargs):
        profile = self.get_object()  # Get the profile for the authenticated user
        serializer = ProfileSerializer(profile, data=request.data, partial=True)  # Allow partial updates

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]

    def update(self, request, *args, **kwargs):
        user = self.get_object()
        serializer = self.get_serializer(user, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)