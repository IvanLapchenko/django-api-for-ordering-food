from django.urls import path
from . import views

urlpatterns = [
    path('create_printer/', views.create_printer, name='create_printer'),
    path('create_check/', views.create_checks, name='create_check'),
]