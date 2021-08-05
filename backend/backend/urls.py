from django.contrib import admin
from django.urls import include, path

from .documentation import schema_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('users.urls')),
    path('api/', include('posts.urls')),
    path('docs/', schema_view.with_ui(
        'swagger', cache_timeout=0), name='schema-swagger-ui')

]
