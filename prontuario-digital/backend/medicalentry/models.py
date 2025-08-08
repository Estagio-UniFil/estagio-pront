from django.db import models
from students.models import Student
from authentication.models import User
from django.utils import timezone

# Create your models here.


class MedicalEntry(models.Model):
    id = models.AutoField(primary_key=True, editable=False, unique=True)
    student = models.ForeignKey(
        Student, on_delete=models.CASCADE, related_name="medical_entries"
    )
    healthpro = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="medical_entries_created"
    )
    entry_date = models.DateTimeField(auto_now_add=True)
    description = models.CharField(max_length=500)
    notes = models.CharField(
        max_length=500,
        null=True,
        db_comment="Additional notes",
        help_text="Observações adicionais",
    )

    deleted = models.BooleanField(default=False)
    deleted_by = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, blank=True
    )
    delete_date = models.DateTimeField(null=True, blank=True)
    delete_reason = models.CharField(max_length=200, null=True, blank=True)

    def soft_delete(self, user, reason):
        self.deleted = True
        self.deleted_by = user
        self.delete_date = timezone.now()
        self.delete_reason = reason
        self.save()

    def __str__(self):
        return self.entry_date
