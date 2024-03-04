from django.contrib import admin
from django.urls import path
import core.api as apps


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', apps.api.urls)
]
