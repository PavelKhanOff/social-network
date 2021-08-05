from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView

from .serializers import CustomTokenObtainPairSerializer


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer


@api_view(['GET', ])
@permission_classes([IsAuthenticated])
def showactivity(request):
    user = request.user
    return Response({
        "last_login": user.last_login,
        "last_made_request": user.last_activity
    })
