from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('', include('app.urls')),
    path('payment/', include('testapp.urls')),
    path('adminapp/', include('adminapp.urls')),
    path('admin/', admin.site.urls),
]
