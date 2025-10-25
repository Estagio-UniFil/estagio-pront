from rest_framework import permissions


class IsAdminUser(permissions.BasePermission):
    """
    Permite acesso apenas para usuários com role 'admin'
    """

    def has_permission(self, request, view):
        if not (request.user and request.user.is_authenticated):
            return False

        return request.user.role == "admin"


class IsHealthProfessionalUser(permissions.BasePermission):
    """
    Permite acesso apenas para usuários com role 'health_prof'
    """

    def has_permission(self, request, view):
        if not (request.user and request.user.is_authenticated):
            return False

        return request.user.role == "health_prof"


class IsAdminOrHealthProfessional(permissions.BasePermission):
    """
    Permite acesso para usuários com role 'admin' ou 'health_prof'
    """

    def has_permission(self, request, view):
        if not (request.user and request.user.is_authenticated):
            return False

        return request.user.role in ["admin", "health_prof"]


class AdminWriteHealthProfRead(permissions.BasePermission):
    """
    Admins: podem fazer tudo (GET, POST, PUT, DELETE)
    Health Professionals: apenas leitura (GET)
    """

    def has_permission(self, request, view):
        if not (request.user and request.user.is_authenticated):
            return False

        if request.method in permissions.SAFE_METHODS:
            return request.user.role in ["admin", "health_prof"]

        return request.user.role == "admin"


class AdminWriteAllRead(permissions.BasePermission):
    """
    Admins: podem fazer tudo (GET, POST, PUT, DELETE)
    Restante: apenas leitura (GET)
    """

    def has_permission(self, request, view):
        if not (request.user and request.user.is_authenticated):
            return False

        if request.method in permissions.SAFE_METHODS:
            return request.user.role in ["admin", "manager", "health_prof"]

        return request.user.role == "admin"


class HealthProfWriteAdminRead(permissions.BasePermission):
    """
    Health Professionals: podem fazer tudo (GET, POST, PUT, DELETE)
    Admins: apenas leitura (GET)
    """

    def has_permission(self, request, view):
        if not (request.user and request.user.is_authenticated):
            return False

        if request.method in permissions.SAFE_METHODS:
            return request.user.role in ["admin", "health_prof"]

        return request.user.role == "health_prof"


class HealthProfWriteAllRead(permissions.BasePermission):
    """
    Todos: podem ler (GET)
    Health Professionals: unico que pode escrever (POST)
    """

    def has_permission(self, request, view):
        if not (request.user and request.user.is_authenticated):
            return False

        if request.method in permissions.SAFE_METHODS:
            return request.user.role in ["admin", "health_prof", "manager"]

        return request.user.role == "health_prof"


class IsManagerUser(permissions.BasePermission):
    """
    Permite acesso apenas para usuários com role 'manager'
    """

    def has_permission(self, request, view):
        if not (request.user and request.user.is_authenticated):
            return False

        return request.user.role == "manager"


class IsAdminOrManager(permissions.BasePermission):
    """
    Permite acesso para usuários com role 'admin' ou 'manager'
    """

    def has_permission(self, request, view):
        if not (request.user and request.user.is_authenticated):
            return False

        return request.user.role in ["admin", "manager"]


class AllRolesRead(permissions.BasePermission):
    """
    Permite leitura para todos os roles autenticados
    """

    def has_permission(self, request, view):
        if not (request.user and request.user.is_authenticated):
            return False

        if request.method in permissions.SAFE_METHODS:
            return request.user.role in ["admin", "manager", "health_prof"]

        return False
