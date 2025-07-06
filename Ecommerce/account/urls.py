from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login_user, name='login'),
    path('logout/', views.logout_user, name='logout'),
    path('register/', views.register_user, name='register'),
    path('user_profile/', views.user_profile, name='user_profile'),
    path('update_password/', views.update_password, name='update_password'),
]