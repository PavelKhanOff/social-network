from django.urls import include, path
from rest_framework_simplejwt.views import TokenRefreshView

from .views import CustomTokenObtainPairView, showactivity

urlpatterns = [
    path('', include('djoser.urls')),
    path('token/', CustomTokenObtainPairView.as_view(), name='get_token'),
    path('token/refresh/', TokenRefreshView.as_view(), name='refresh_token'),
    path('user/activity/', showactivity, name='activity')
]
