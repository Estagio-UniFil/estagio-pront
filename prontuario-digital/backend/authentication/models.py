from django.db import models
from django.contrib.auth.models import AbstractUser
import uuid
from rest_framework.authtoken.models import Token as DRFToken
from datetime import timedelta
from django.utils import timezone


# Create your models here.


class User(AbstractUser):
    ROLE_CHOICES = (
        ("admin", "Administrador"),
        ("manager", "Gestor"),
        ("health_prof", "Profissional da Saúde"),
    )
    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False, unique=True
    )
    role = models.CharField(max_length=11, choices=ROLE_CHOICES)
    email = models.EmailField(unique=True, verbose_name="E-mail")

    USERNAME_FIELD = "email"

    REQUIRED_FIELDS = ["first_name", "last_name", "role"]

    def __str__(self):
        return self.email


class HealthProfile(models.Model):
    ESPECIALITY_CHOICES = (
        ("psychologist", "Psicologia"),
        ("physiotherapist", "Fisioterapia"),
        ("social_worker", "Assistencia Social"),
        ("speech_therapist", "Fonoaudiologia"),
    )

    user = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name="health_profile"
    )
    specialty = models.CharField(max_length=100, verbose_name="Especialidade")
    council_number = models.CharField(max_length=20)

    def __str__(self):
        return f"{self.user.get_full_name()} ({self.specialty})"


class Token(DRFToken):
    def is_expired(self):
        # Tempo de vida do token
        token_lifetime = timedelta(seconds=10)
        return timezone.now() > self.created + token_lifetime
