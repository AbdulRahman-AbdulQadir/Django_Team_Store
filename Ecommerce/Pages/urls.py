from django.urls import path
from . import views

urlpatterns = [
    path('', views.home),
    path('contact_us', views.contact_us ),
    path('about', views.about),
]