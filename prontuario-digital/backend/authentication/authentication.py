from rest_framework.authentication import TokenAuthentication
from rest_framework import exceptions
from .models import Token


class ExpiringTokenAuthentication(TokenAuthentication):
    model = Token

    def authenticate_credentials(self, key):
        try:
            token = self.model.objects.select_related("user").get(key=key)
        except self.model.DoesNotExist:
            raise exceptions.AuthenticationFailed("Ivalid token.")

        if not token.user.is_active:
            raise exceptions.AuthenticationFailed("Inactive user.")

        if token.is_expired():
            token.delete()
            raise exceptions.AuthenticationFailed("Expired token.")

        return (token.user, token)
