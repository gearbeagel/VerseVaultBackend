from django.urls import path

from misc import views

urlpatterns = [
    path('csrf/', views.csrf, name='csrf'),
    path('user_check/', views.user_check, name='user_check'),
    path('current_user/', views.current_user, name='current_user'),
]