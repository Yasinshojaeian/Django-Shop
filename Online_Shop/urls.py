from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include

from Online_Shop import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('home.urls')),
    path('accounts/', include('accounts.urls')),
    path('orders/', include('orders.urls')),
]+ static(settings.MEDIA_URL , document_root = settings.MEDIA_ROOT)
