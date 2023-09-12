from .views import admin_view
from django.urls import path

urlpatterns = [
    path('', admin_view),
]