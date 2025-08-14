from rest_framework import status
from rest_framework.test import APITestCase
from django.urls import reverse
from medicalentry.models import MedicalEntry
from students.models import Student
from authentication.models import User, HealthProfile
from datetime import date


class MedicalEntryTests(APITestCase):
    @classmethod
    def setUpTestData(cls):
        # Criação de usuários e perfis para os testes
        cls.admin_user = User.objects.create_user(
            username="admin",  # Adicionado o username
            email="admin@example.com",
            password="testpassword123",
            role="admin",
            first_name="Admin",
            last_name="User",
        )

        cls.health_prof_user_psychologist = User.objects.create_user(
            username="psycho",  # Adicionado o username
            email="psycho@example.com",
            password="testpassword123",
            role="health_prof",
            first_name="Psycho",
            last_name="Prof",
        )
        HealthProfile.objects.create(
            user=cls.health_prof_user_psychologist,
            specialty="psychologist",
            council_number="12345",
        )

        cls.health_prof_user_physiotherapist = User.objects.create_user(
            username="physio",  # Adicionado o username
            email="physio@example.com",
            password="testpassword123",
            role="health_prof",
            first_name="Physio",
            last_name="Prof",
        )
        HealthProfile.objects.create(
            user=cls.health_prof_user_physiotherapist,
            specialty="physiotherapist",
            council_number="67890",
        )

        cls.other_user = User.objects.create_user(
            username="manager",  # Adicionado o username
            email="manager@example.com",
            password="testpassword123",
            role="manager",
            first_name="Manager",
            last_name="User",
        )

        # Criação de um estudante para os testes
        cls.student = Student.objects.create(
            name="Test Student",
            cgm="1234567890",
            dob=date(2000, 1, 1),
            gender="M",
            guardian="Guardian",
            guardian_cpf="12345678901",
            address="Test Address",
            cep="12345678",
            city="Test City",
            state="TS",
        )

        # Criação de entradas médicas para os testes
        cls.medical_entry_psychologist = MedicalEntry.objects.create(
            student=cls.student,
            healthpro=cls.health_prof_user_psychologist,
            description="Psychological evaluation",
            notes="Patient shows good progress.",
        )
        cls.medical_entry_physiotherapist = MedicalEntry.objects.create(
            student=cls.student,
            healthpro=cls.health_prof_user_physiotherapist,
            description="Physiotherapy session",
            notes="Focus on motor skills.",
        )

    def test_get_medical_entries_as_admin_no_student_id(self):
        self.client.force_authenticate(user=self.admin_user)
        url = reverse("medical_entry_list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_get_medical_entries_as_health_prof_no_student_id(self):
        self.client.force_authenticate(user=self.health_prof_user_psychologist)
        url = reverse("medical_entry_list")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["description"], "Psychological evaluation")

    def test_get_medical_entries_as_admin_with_student_id(self):
        self.client.force_authenticate(user=self.admin_user)
        url = reverse("medical_entry_list")
        response = self.client.get(f"{url}?student_id={self.student.id}")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_get_medical_entries_as_health_prof_with_student_id(self):
        self.client.force_authenticate(user=self.health_prof_user_psychologist)
        url = reverse("medical_entry_list")
        response = self.client.get(f"{url}?student_id={self.student.id}")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["description"], "Psychological evaluation")

    def test_post_medical_entry_as_health_prof(self):
        self.client.force_authenticate(user=self.health_prof_user_psychologist)
        url = reverse("medical_entry_list")
        payload = {
            "description": "New entry by health professional",
            "notes": "Follow up next week.",
        }
        response = self.client.post(
            f"{url}?student_id={self.student.id}", payload, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(MedicalEntry.objects.count(), 3)
        self.assertEqual(
            response.data["description"], "New entry by health professional"
        )

    def test_post_medical_entry_without_student_id_fails(self):
        self.client.force_authenticate(user=self.health_prof_user_psychologist)
        url = reverse("medical_entry_list")
        payload = {
            "description": "New entry without a student",
        }
        response = self.client.post(url, payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data["detail"], "No informed student")

    def test_get_medical_entries_as_other_user_forbidden(self):
        self.client.force_authenticate(user=self.other_user)
        url = reverse("medical_entry_list")
        response = self.client.get(f"{url}?student_id={self.student.id}")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_post_medical_entry_as_other_user_forbidden(self):
        self.client.force_authenticate(user=self.other_user)
        url = reverse("medical_entry_list")
        payload = {
            "description": "Forbidden entry",
        }
        response = self.client.post(
            f"{url}?student_id={self.student.id}", payload, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class MedicalEntryDetailTests(APITestCase):
    @classmethod
    def setUpTestData(cls):
        # Similar setup para a classe de detalhes
        cls.admin_user = User.objects.create_user(
            username="admin",  # Adicionado o username
            email="admin@example.com",
            password="testpassword123",
            role="admin",
            first_name="Admin",
            last_name="User",
        )

        cls.health_prof_user_psychologist = User.objects.create_user(
            username="psycho",  # Adicionado o username
            email="psycho@example.com",
            password="testpassword123",
            role="health_prof",
            first_name="Psycho",
            last_name="Prof",
        )
        HealthProfile.objects.create(
            user=cls.health_prof_user_psychologist,
            specialty="psychologist",
            council_number="12345",
        )

        cls.health_prof_user_physiotherapist = User.objects.create_user(
            username="physio",  # Adicionado o username
            email="physio@example.com",
            password="testpassword123",
            role="health_prof",
            first_name="Physio",
            last_name="Prof",
        )
        HealthProfile.objects.create(
            user=cls.health_prof_user_physiotherapist,
            specialty="physiotherapist",
            council_number="67890",
        )

        cls.other_user = User.objects.create_user(
            username="manager",  # Adicionado o username
            email="manager@example.com",
            password="testpassword123",
            role="manager",
            first_name="Manager",
            last_name="User",
        )

        cls.student = Student.objects.create(
            name="Test Student",
            cgm="1234567890",
            dob=date(2000, 1, 1),
            gender="M",
            guardian="Guardian",
            guardian_cpf="12345678901",
            address="Test Address",
            cep="12345678",
            city="Test City",
            state="TS",
        )

        cls.medical_entry_psychologist = MedicalEntry.objects.create(
            student=cls.student,
            healthpro=cls.health_prof_user_psychologist,
            description="Psychological evaluation",
            notes="Patient shows good progress.",
        )

        cls.medical_entry_physiotherapist = MedicalEntry.objects.create(
            student=cls.student,
            healthpro=cls.health_prof_user_physiotherapist,
            description="Physiotherapy session",
            notes="Focus on motor skills.",
        )

    def test_get_medical_entry_as_admin(self):
        self.client.force_authenticate(user=self.admin_user)
        url = reverse("medical_entry_detail", args=[self.medical_entry_psychologist.pk])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["description"], "Psychological evaluation")

    def test_get_medical_entry_as_health_prof_same_specialty(self):
        self.client.force_authenticate(user=self.health_prof_user_psychologist)
        url = reverse("medical_entry_detail", args=[self.medical_entry_psychologist.pk])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["description"], "Psychological evaluation")

    def test_get_medical_entry_as_health_prof_different_specialty_forbidden(self):
        self.client.force_authenticate(user=self.health_prof_user_physiotherapist)
        url = reverse("medical_entry_detail", args=[self.medical_entry_psychologist.pk])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response.data["detail"], "This is not in your scope")

    def test_delete_medical_entry_as_admin(self):
        self.client.force_authenticate(user=self.admin_user)
        url = reverse("medical_entry_detail", args=[self.medical_entry_psychologist.pk])
        payload = {"delete_reason": "Entry is obsolete."}
        response = self.client.delete(url, payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        entry = MedicalEntry.objects.get(pk=self.medical_entry_psychologist.pk)
        self.assertTrue(entry.deleted)
        self.assertEqual(entry.delete_reason, "Entry is obsolete.")
        self.assertEqual(entry.deleted_by, self.admin_user)

    def test_delete_medical_entry_as_health_prof(self):
        self.client.force_authenticate(user=self.health_prof_user_psychologist)
        url = reverse("medical_entry_detail", args=[self.medical_entry_psychologist.pk])
        payload = {"delete_reason": "Correction needed."}
        response = self.client.delete(url, payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        entry = MedicalEntry.objects.get(pk=self.medical_entry_psychologist.pk)
        self.assertTrue(entry.deleted)
        self.assertEqual(entry.delete_reason, "Correction needed.")
        self.assertEqual(entry.deleted_by, self.health_prof_user_psychologist)

    def test_delete_medical_entry_without_reason_fails(self):
        self.client.force_authenticate(user=self.admin_user)
        url = reverse("medical_entry_detail", args=[self.medical_entry_psychologist.pk])
        payload = {}
        response = self.client.delete(url, payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data["detail"], "Delete reason is mandatory")

    def test_delete_already_deleted_entry_fails(self):
        self.medical_entry_psychologist.soft_delete(self.admin_user, "Initial deletion")
        self.client.force_authenticate(user=self.admin_user)
        url = reverse("medical_entry_detail", args=[self.medical_entry_psychologist.pk])
        payload = {"delete_reason": "Second deletion."}
        response = self.client.delete(url, payload, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data["detail"], "Entry is already deleted")

    def test_get_deleted_entry_as_admin_forbidden(self):
        self.medical_entry_psychologist.soft_delete(self.admin_user, "Initial deletion")
        self.client.force_authenticate(user=self.admin_user)
        url = reverse("medical_entry_detail", args=[self.medical_entry_psychologist.pk])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data["detail"], "Medical entry not found")
