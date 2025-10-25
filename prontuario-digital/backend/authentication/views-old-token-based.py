from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework.decorators import api_view, permission_classes
from .models import User
from rest_framework import status
from .serializers import UserSerializer
from authentication.permissions import (
    IsManagerUser,
    IsAdminUser,
    AdminWriteAllRead,
)

# Create your views here.


class CustomAuthToken(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(
            data=request.data, context={"request": request}
        )
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]
        token, created = Token.objects.get_or_create(user=user)

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


@permission_classes([AdminWriteAllRead])
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all().order_by("first_name")
    serializer_class = UserSerializer
    permission_classes = [IsAdminUser]


@api_view(["GET"])
@permission_classes([IsManagerUser])
def view_health_pros(request):
    if request.method == "GET":
        queryset = User.objects.filter(role="health_prof").order_by("first_name")
        serializer = UserSerializer(queryset, many=True)
        return Response(
            serializer.data,
            status=status.HTTP_200_OK,
        )
