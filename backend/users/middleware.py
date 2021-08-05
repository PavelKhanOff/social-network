from django.contrib.auth.models import AnonymousUser
from django.utils import timezone
from rest_framework_simplejwt.authentication import JWTAuthentication


class UpdateLastActivityMiddleware(object):

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        return self.get_response(request)

    def process_view(self, request, view_func, view_args, view_kwargs):
        user = AnonymousUser
        try:
            user = JWTAuthentication().authenticate(request)[0]
        except Exception:
            pass
        if user is not AnonymousUser:
            user.last_activity = timezone.now()
            user.save()
