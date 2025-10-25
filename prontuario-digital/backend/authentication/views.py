from django.contrib.auth import authenticate, login, logout
from django.middleware.csrf import get_token
from django.views.decorators.csrf import ensure_csrf_cookie
from rest_framework.decorators import api_view, permission_classes, action
from rest_framework.permissions import AllowAny
from rest_framework.permissions import IsAuthenticated as DRFIsAuthenticated
from rest_framework.response import Response
from rest_framework import status, viewsets
from .models import User
from .serializers import (
    UserSerializer,
    MeSerializer,
    PasswordChangeSerializer,
    AdminPasswordResetSerializer,
)
from authentication.permissions import IsManagerUser, AdminWriteAllRead, IsAdminUser


class SessionLoginView:
    """
    View de Login com Sessions
    """

    @api_view(["POST"])
    @permission_classes([AllowAny])
    @ensure_csrf_cookie
    def login_view(request):
        """
        Login - Cira e inicia a sessão
        """
        email = request.data.get("email")
        password = request.data.get("password")
        remember_me = request.data.get("remember_me", False)

        if not email or not password:
            return Response(
                {"error": "Email e senha são obrigatórios"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Email auth
        user = authenticate(request, username=email, password=password)

        if user is not None:
            login(request, user)

            if remember_me:
                # 30 days if rememberMe
                request.session.set_expiry(2592000)  # In seconds
            else:
                # Session expires when closing browser
                request.session.set_expiry(0)

            # User Data Serializer
            user_data = {
                "user_id": str(user.pk),
                "email": user.email,
                "first_name": user.first_name,
                "last_name": user.last_name,
                "role": user.role,
                "session_expiry": "persistent" if remember_me else "browser_close",
                "must_change_password": user.must_change_password,
            }

            # Health Pro data
            if user.role == "health_prof" and hasattr(user, "health_profile"):
                user_data["health_profile"] = {
                    "specialty": user.health_profile.specialty,
                    "council_number": user.health_profile.council_number,
                }

            return Response(user_data, status=status.HTTP_200_OK)

        return Response(
            {"error": "Credenciais inválidas"}, status=status.HTTP_401_UNAUTHORIZED
        )

    @api_view(["POST"])
    @permission_classes([AllowAny])
    def logout_view(request):
        """
        Logout - encerra a sessão
        """
        logout(request)
        return Response(
            {"message": "Logout realizado com sucesso"}, status=status.HTTP_200_OK
        )

    @api_view(["GET"])
    @ensure_csrf_cookie
    @permission_classes([AllowAny])
    def get_csrf_token(request):
        """
        Endpoint para obter o CSRF token
        Para o frontend pegar o token antes de fazer login
        """
        return Response({"csrfToken": get_token(request)})

    @api_view(["GET"])
    def check_auth(request):
        """
        Verifica se o usuário está autenticado
        """
        if request.user.is_authenticated:
            user_data = {
                "user_id": str(request.user.pk),
                "email": request.user.email,
                "first_name": request.user.first_name,
                "last_name": request.user.last_name,
                "role": request.user.role,
                "is_authenticated": True,
                "must_change_password": request.user.must_change_password,
            }

            if request.user.role == "health_prof" and hasattr(
                request.user, "health_profile"
            ):
                user_data["health_profile"] = {
                    "specialty": request.user.health_profile.specialty,
                    "council_number": request.user.health_profile.council_number,
                }
            return Response(user_data, status=status.HTTP_200_OK)

        return Response(
            {"is_authenticated": False}, status=status.HTTP_401_UNAUTHORIZED
        )


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all().order_by("first_name")
    serializer_class = UserSerializer
    permission_classes = [AdminWriteAllRead]

    @action(
        detail=True,
        methods=["post"],
        permission_classes=[IsAdminUser],
        url_path="reset-password",
    )
    def reset_password(self, request, pk=None):
        """
        Endpoint para um Admin redefinir a senha de um usuário específico.
        """
        user = self.get_object()
        serializer = AdminPasswordResetSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        new_password = serializer.validated_data["new_password"]

        user.set_password(new_password)

        user.must_change_password = True
        user.save(update_fields=["password", "must_change_password"])

        return Response(
            {"message": f"Senha do usuário {user.email} redefinida com sucesso."},
            status=status.HTTP_200_OK,
        )

    @action(
        detail=False,
        methods=["get", "patch"],
        permission_classes=[DRFIsAuthenticated],
        url_path="me",
    )
    def me(self, request):
        """
        GET: retorna dados do usuário autenticado (limitados)
        PATCH: atualiza email, first_name e last_name do próprio usuário
        """
        user = request.user
        if request.method == "GET":
            return Response(MeSerializer(user).data, status=status.HTTP_200_OK)

        serializer = MeSerializer(
            user, data=request.data, partial=True, context={"request": request}
        )
        if serializer.is_valid():
            serializer.save()
            print(serializer.data)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @action(
        detail=False,
        methods=["post"],
        permission_classes=[DRFIsAuthenticated],
        url_path="set-password",
    )
    def set_password(self, request):
        """
        Endpoint para o usuário logado definir ou alterar sua própria senha.
        """
        user = request.user
        serializer = PasswordChangeSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        new_password = serializer.validated_data["new_password"]

        if user.must_change_password:
            user.set_password(new_password)
            user.must_change_password = False
            user.save()
            return Response(
                {"message": "Senha definida com sucesso."}, status=status.HTTP_200_OK
            )

        current_password = serializer.validated_data.get("current_password")
        if not current_password:
            return Response(
                {"error": "A senha atual é obrigatória."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        if not user.check_password(current_password):
            return Response(
                {"error": "A senha atual está incorreta."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        user.set_password(new_password)
        user.save()
        return Response(
            {"message": "Senha alterada com sucesso."}, status=status.HTTP_200_OK
        )

    @action(
        detail=False,
        methods=["get"],
        permission_classes=[IsManagerUser],
        url_path="managerview",
    )
    def view_health_pros(self, request):
        queryset = User.objects.filter(role="health_prof").order_by("first_name")
        serializer = UserSerializer(queryset, many=True)
        return Response(
            serializer.data,
            status=status.HTTP_200_OK,
        )
