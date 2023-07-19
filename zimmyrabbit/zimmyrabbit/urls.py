from django.urls import path
from . import views

app_name = 'zimmyrabbit'

urlpatterns = [
    path('', views.index, name="index"),
    path('check_model/', views.check_model, name="check_model"),
]