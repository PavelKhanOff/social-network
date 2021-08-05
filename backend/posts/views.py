from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status, viewsets
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .filters import LikeFilter
from .models import Like, Post
from .permissions import AdminOrAuthorOrReadOnly
from .serializers import (CreateUpdateDeletePostSerializer, LikeSerializer,
                          ShowPostSerializer)


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    permission_classes = (AdminOrAuthorOrReadOnly, )

    def get_serializer_context(self):
        context = super().get_serializer_context()
        context.update({'request': self.request})
        return context

    def get_serializer_class(self):
        if self.action in ['list', 'retrieve']:
            return ShowPostSerializer
        return CreateUpdateDeletePostSerializer


class LikeViewSet(APIView):
    permission_classes = (IsAuthenticated, )

    def get(self, request, post_id):
        user = request.user
        post = get_object_or_404(Post, id=post_id)
        if Like.objects.filter(user=user, post=post).exists():
            return Response(
                'Вы уже лайкнули этот пост',
                status=status.HTTP_400_BAD_REQUEST)
        Like.objects.create(user=user, post=post)
        return Response(
            'Лайк успешно поставлен', status=status.HTTP_201_CREATED)

    def delete(self, request, post_id):
        user = request.user
        post = get_object_or_404(Post, id=post_id)
        like_obj = get_object_or_404(Like, user=user, post=post)
        like_obj.delete()
        return Response('Удалено', status=status.HTTP_204_NO_CONTENT)


class LikeAnalyticsViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Like.objects.all()
    serializer_class = LikeSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = LikeFilter
    permission_classes = (AllowAny, )
