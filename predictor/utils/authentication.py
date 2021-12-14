
from rest_framework.authentication import BasicAuthentication
from .. import models

class UserAnthenticate(BasicAuthentication):

    def authenticate(self, req):
        token = req.META.get('HTTP_AUTHORIZATION')

        if token:
            token = token.split()[1]
            token_obj = models.UserToken.objects.filter(token=token).first()
            if token_obj:
                return (token_obj.user, token_obj)
        return (None, None)

    def authenticate_header(self, request):
        pass

__all__ = [UserAnthenticate, ]
