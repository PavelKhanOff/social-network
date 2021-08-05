from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import LikeAnalyticsViewSet, LikeViewSet, PostViewSet

router = DefaultRouter()
router.register('posts', PostViewSet, basename='posts')


urlpatterns = [
    path('posts/<int:post_id>/like/', LikeViewSet.as_view(), name='post_like'),
    path('like/analytics/', LikeAnalyticsViewSet.as_view({'get': 'list'}),
         name='like_analytics'),
    path('', include(router.urls))
]
