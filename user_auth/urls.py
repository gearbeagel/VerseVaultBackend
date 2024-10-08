"""
URL configuration for backend project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter

from user_auth import views
from user_auth.views import *

router = DefaultRouter()
router.register(r"profile", ProfileViewSet, basename="profile")
router.register(r"user", UserViewSet, basename="user")
router.register(r"writerstats", WriterStatsViewSet, basename="writerstats")
router.register(r"readerstats", ReaderStatsViewSet, basename="readerstats")
router.register(r'favs', FavoriteViewSet, basename="favs")

urlpatterns = [
    path('', include(router.urls)),
    path('register/', views.RegistrationView.as_view(), name='register'),
    path("login/", views.LoginView.as_view(), name="login"),
    path("google_login/", views.GoogleLogin.as_view(), name="google_login"),
    path("logout/", views.LogoutView.as_view(), name="logout"),
]
