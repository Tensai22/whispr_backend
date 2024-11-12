from django.contrib import admin
from django.urls import path, include
from django.conf.urls import include
urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('logic.urls')),
    path('api-auth/', include('rest_framework.urls')),
    path('chat/', include('chat.urls')),
]
