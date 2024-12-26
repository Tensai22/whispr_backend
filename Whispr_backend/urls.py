from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from logic.views import UserDetailView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('logic.urls')),
    path('api-auth/', include('rest_framework.urls')),
    path('chat/', include('chat.urls')),  # Подключение приложения chat
    path('api/user/<int:pk>/', UserDetailView.as_view(), name='user-detail'),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)