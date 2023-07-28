from django.urls import path
from . import views
from .views import BuildHistList, BuildHistDetail

app_name = 'zimmyrabbit'

urlpatterns = [
    path('', views.index, name="index"),
    path('check_model/', views.check_model, name="check_model"),
    path('request_build/', views.request_build, name="request_build"),
    path('buildHist/', BuildHistList.as_view()),
    path('buildHist/<int:pk>/', BuildHistDetail.as_view()),
]