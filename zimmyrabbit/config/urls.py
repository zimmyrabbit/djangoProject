from django.contrib import admin
from django.urls import path
from zimmyrabbit import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('zimmyrabbit/', views.index),
]
