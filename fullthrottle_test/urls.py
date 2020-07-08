from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('fullthrottle/', include('fullthrottle.urls')),
    path('admin/', admin.site.urls),
]