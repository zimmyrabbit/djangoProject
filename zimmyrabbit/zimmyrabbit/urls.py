from django.urls import path
from . import views
from .views import BuildHistList, BuildHistDetail

app_name = 'zimmyrabbit'

urlpatterns = [
    path('', views.index, name="index"),
    path('check_model/', views.check_model, name="check_model"),
    path('buildHist/', BuildHistList.as_view()),
    path('buildHist/<int:pk>/', BuildHistDetail.as_view()),
]