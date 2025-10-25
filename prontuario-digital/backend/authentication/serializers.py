from rest_framework import serializers
from .models import User, HealthProfile


class HealthProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = HealthProfile
        fields = ["specialty", "council_number"]


class UserSerializer(serializers.ModelSerializer):
    health_profile = HealthProfileSerializer(required=False, allow_null=True)

    class Meta:
        model = User
        fields = [
            "id",
            "username",
            "email",
            "first_name",
            "last_name",
            "role",
            "password",
            "health_profile",
            "must_change_password",
        ]
        extra_kwargs = {
            "password": {"write_only": True, "style": {"input_type": "password"}},
            "username": {"required": False},
            "must_change_password": {"read_only": True},
        }

    def create(self, validated_data):
        """
        O pop aqui separa o health_profile do restante do payload
        Pq users não possuem esse campo, então causaria erro no create user
        Caso a chave esteja vazia o valor padrão é None
        """
        profile_data = validated_data.pop("health_profile", None)

        """
        Caso username não seja passado no payload
        Geração de username automático: nome.role 
        Usuário padrão do Django pede um username
        """
        if not validated_data.get("username"):
            role_map = {"admin": "adm", "manager": "man", "health_prof": "hp"}
            first_name = validated_data.get("first_name", "").lower()
            role = validated_data.get("role", "")

            base_username = f"{first_name}.{role_map.get(role, role)}"
            username = base_username
            counter = 1

            while User.objects.filter(username=username).exists():
                username = f"{base_username}{counter}"
                counter += 1

            validated_data["username"] = username

        # Create_user method to hash the password
        user = User.objects.create_user(**validated_data)

        user.must_change_password = True
        user.save(update_fields=["must_change_password"])

        if user.role == "health_prof" and profile_data:
            HealthProfile.objects.create(user=user, **profile_data)
        elif user.role == "health_prof" and not profile_data:
            user.delete()
            raise serializers.ValidationError(
                "Dados do perfil profissional são obrigatórios."
            )

        return user

    def update(self, instance, validated_data):
        profile_data = validated_data.pop("health_profile", None)
        password = validated_data.pop("password", None)

        instance = super().update(instance, validated_data)

        if password:
            instance.set_password(password)
            instance.must_change_password = False
            instance.save()

        if instance.role == "health_prof":
            if profile_data:
                profile, created = HealthProfile.objects.update_or_create(
                    user=instance, defaults=profile_data
                )

        return instance


class MeSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["email", "first_name", "last_name"]
        extra_kwargs = {
            "email": {"required": True},
            "first_name": {"required": False, "allow_blank": True},
            "last_name": {"required": False, "allow_blank": True},
        }

    def validate_email(self, value):
        user = self.context["request"].user
        if User.objects.exclude(pk=user.pk).filter(email=value).exists():
            raise serializers.ValidationError("Este e-mail já está em uso.")
        return value


class PasswordChangeSerializer(serializers.Serializer):
    """
    Serializer para o endpoint de alteração de senha.
    Valida a nova senha e a confirmação.
    A senha atual é opcional para o caso do primeiro login.
    """

    current_password = serializers.CharField(
        style={"input_type": "password"}, required=False, allow_blank=True
    )
    new_password = serializers.CharField(
        style={"input_type": "password"}, required=True
    )
    confirm_password = serializers.CharField(
        style={"input_type": "password"}, required=True
    )

    def validate(self, data):
        if data["new_password"] != data["confirm_password"]:
            raise serializers.ValidationError(
                {"confirm_password": "As senhas não coincidem."}
            )
        return data


class AdminPasswordResetSerializer(serializers.Serializer):
    """
    Serializer para o Admin redefinir a senha de um usuário.
    Não pede a senha atual.
    """

    new_password = serializers.CharField(
        style={"input_type": "password"}, required=True
    )
    confirm_password = serializers.CharField(
        style={"input_type": "password"}, required=True
    )

    def validate(self, data):
        if data["new_password"] != data["confirm_password"]:
            raise serializers.ValidationError(
                {"confirm_password": "As senhas não coincidem."}
            )
        return data


class UserNestedSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["id", "first_name", "last_name"]
