from django.urls import path
from . import views

urlpatterns = [
    path('create_printer/', views.create_printer, name='create_printer'),
    # path('generate_check/<int:order_id>/', views.generate_check, name='generate_check'),
]