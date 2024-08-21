from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render
from django.views import View
from django.views.decorators.csrf import ensure_csrf_cookie, csrf_exempt


# Create your views here.

def index(request):
    return HttpResponse("Hello World.")


@ensure_csrf_cookie
def csrf(request):
    return JsonResponse({"message": "CSRF cookie set"})


@csrf_exempt
def user_check(request):
    return JsonResponse({'is_authenticated': request.user.is_authenticated})


@login_required
def current_user(request):
    user = request.user
    user_data = {
        'id': user.profile.id,
        'username': user.username,
        'email': user.email,
    }
    return JsonResponse(user_data)
