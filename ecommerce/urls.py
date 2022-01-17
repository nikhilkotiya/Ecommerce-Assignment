from django.conf import settings
from django.contrib import admin
from django.conf.urls.static import static
from django.urls import path,include
# from django.urls import path
# from .import views
# from allauth.account.views import confirm_email
from django.conf.urls import url
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('api.urls')),    
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)