
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('stock/', include('predictor.urls')),
    path('uploader/', include('uploader.urls')),
]
