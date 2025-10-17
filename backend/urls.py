"""
URL configuration for backend project.
"""
from django.contrib import admin
from django.urls import path, include
from django.http import JsonResponse
from django.conf import settings
from django.conf.urls.static import static


# Home view for root URL
def home(request):
    return JsonResponse({
        "status": "ok",
        "message": "Exact Match Backend is live 🚀"
    })


urlpatterns = [
    path('', home, name='home'),              # 👈 Root route added here
    path('admin/', admin.site.urls),
    path('api/', include('batteries.urls')),
]

# Serve media files in development
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
