from django.contrib import admin
from django.urls import path, include
from zimmyrabbit import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('zimmyrabbit/', include('zimmyrabbit.urls')),
]
