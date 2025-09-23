from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework.decorators import api_view, permission_classes
from .models import User
from .serializers import UserSerializer
from authentication.permissions import (
    IsManagerUser,
    IsAdminUser,
)

# Create your views here.


class CustomAuthToken(ObtainAuthToken):
    # View de Login: Recebe email e senha, retorna Token.
    def post(self, request, *args, **kwargs):
        # Usa o serializer padrão do DRF
        serializer = self.serializer_class(
            data=request.data, context={"request": request}
        )
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]
        token, created = Token.objects.get_or_create(user=user)

        # Retorna o token e a role para permissões
        return Response(
            {
                "token": token.key,
                "user_id": user.pk,
                "email": user.email,
                "first_name": user.first_name,
                "last_name": user.last_name,
                "role": user.role,
            }
        )


@permission_classes([IsAdminUser])
class UserViewSet(viewsets.ModelViewSet):
    # Endpoint para admins gerenciarem users
    queryset = User.objects.all().order_by("first_name")
    serializer_class = UserSerializer
    permission_classes = [IsAdminUser]


@api_view(["GET"])
@permission_classes([IsManagerUser])
def view_health_pros(request):
    queryset = User.objects.filter(role="health_professional").order_by("first_name")
    serializer = UserSerializer(queryset, many=True)
    return Response(serializer.data)
