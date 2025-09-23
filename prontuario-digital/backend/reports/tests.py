from django.test import TestCase, RequestFactory
from django.contrib.auth import get_user_model
from django.utils import timezone
from datetime import date
from unittest.mock import patch, Mock

from rest_framework.test import APITestCase, APIClient
from rest_framework import status

from .views import ExcelRenderer
from .models import ReportLog
from medicalentry.models import MedicalEntry
from students.models import Student


class ExcelRendererTestCase(TestCase):
    """Testes para a classe ExcelRenderer"""

    def setUp(self):
        self.renderer = ExcelRenderer()

    def test_excel_renderer_attributes(self):
        """Testa se os atributos da classe estão corretos"""
        self.assertEqual(
            self.renderer.media_type,
            "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        )
        self.assertEqual(self.renderer.format, "xlsx")
        self.assertIsNone(self.renderer.charset)
        self.assertEqual(self.renderer.render_style, "binary")

    def test_render_method(self):
        """Testa se o método render retorna os dados sem modificação"""
        test_data = b"test_excel_data"
        result = self.renderer.render(test_data)
        self.assertEqual(result, test_data)

    def test_render_method_with_optional_params(self):
        """Testa o método render com parâmetros opcionais"""
        test_data = b"test_excel_data"
        result = self.renderer.render(
            test_data,
            media_type="application/excel",
            renderer_context={"request": Mock()},
        )
        self.assertEqual(result, test_data)


class MonthlyReportTestCase(APITestCase):
    """Testes para a view monthly_report"""

    def setUp(self):
        self.factory = RequestFactory()
        self.client = APIClient()

        # Criar usuário de teste com modelo personalizado
        User = get_user_model()
        self.user = User.objects.create_user(
            username="testuser",
            email="test@example.com",
            password="testpass123",
            first_name="Test",
            last_name="User",
            role="health_prof",
        )

        # Criar estudante de teste com campos corretos
        self.student = Student.objects.create(
            name="João Silva",
            cgm="1234567890",
            dob=date(2000, 1, 1),
            gender="M",
            guardian="Maria Silva",
            guardian_cpf="98765432100",
            address="Rua Teste, 123",
            cep="12345678",
            city="São Paulo",
            state="SP",
            created_by=self.user,
            updated_by=self.user,
        )

        # Criar entrada médica de teste
        self.medical_entry = MedicalEntry.objects.create(
            student=self.student,
            healthpro=self.user,
            description="Consulta de rotina",
            entry_date=timezone.now(),
        )

    def test_monthly_report_without_params(self):
        """Testa relatório mensal sem parâmetros (mês atual)"""
        self.client.force_authenticate(user=self.user)

        with patch("reports.views.MedicalEntry.objects.filter") as mock_filter:
            mock_filter.return_value.order_by.return_value = [self.medical_entry]

            response = self.client.get("/api/reports/medical-entries/monthly/")

            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertEqual(
                response["Content-Type"],
                "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            )
            self.assertIn("attachment", response["Content-Disposition"])

    def test_monthly_report_with_valid_params(self):
        """Testa relatório mensal com parâmetros válidos"""
        self.client.force_authenticate(user=self.user)

        with patch("reports.views.MedicalEntry.objects.filter") as mock_filter:
            mock_filter.return_value.order_by.return_value = [self.medical_entry]

            response = self.client.get(
                "/api/reports/medical-entries/monthly/?year=2023&month=12"
            )

            self.assertEqual(response.status_code, status.HTTP_200_OK)
            mock_filter.assert_called_once()

    def test_monthly_report_with_invalid_params(self):
        """Testa relatório mensal com parâmetros inválidos"""
        self.client.force_authenticate(user=self.user)

        response = self.client.get(
            "/api/reports/medical-entries/monthly/?year=invalid&month=invalid"
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data["detail"], "Parameters must be integers")

    def test_monthly_report_creates_log(self):
        """Testa se o relatório mensal cria um log"""
        self.client.force_authenticate(user=self.user)

        with patch("reports.views.MedicalEntry.objects.filter") as mock_filter:
            mock_filter.return_value.order_by.return_value = []

            initial_log_count = ReportLog.objects.count()
            response = self.client.get("/api/reports/medical-entries/monthly/")

            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertEqual(ReportLog.objects.count(), initial_log_count + 1)

            log = ReportLog.objects.latest("date")
            self.assertEqual(log.user_id, self.user)
            self.assertEqual(log.report_type, ReportLog.ReportTypes.GENERAL_MONTHLY)

    @patch("reports.views.Workbook")
    def test_monthly_report_excel_generation(self, mock_workbook):
        """Testa a geração do arquivo Excel no relatório mensal"""
        self.client.force_authenticate(user=self.user)

        # Mock do workbook
        mock_wb = Mock()
        mock_sheet = Mock()
        mock_wb.active = mock_sheet
        mock_workbook.return_value = mock_wb

        # Mock do buffer
        mock_buffer = Mock()
        mock_buffer.getvalue.return_value = b"excel_content"

        with (
            patch("reports.views.MedicalEntry.objects.filter") as mock_filter,
            patch("reports.views.io.BytesIO", return_value=mock_buffer),
        ):
            mock_filter.return_value.order_by.return_value = [self.medical_entry]

            self.client.get("/api/reports/medical-entries/monthly/")

            # Verificar se o workbook foi configurado corretamente
            mock_sheet.append.assert_called()
            mock_wb.save.assert_called_once_with(mock_buffer)
            mock_buffer.seek.assert_called_once_with(0)

    def test_monthly_report_unauthenticated(self):
        """Testa acesso não autenticado ao relatório mensal"""
        response = self.client.get("/api/reports/medical-entries/monthly/")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class StudentIntervalReportTestCase(APITestCase):
    """Testes para a view student_interval_report"""

    def setUp(self):
        self.factory = RequestFactory()
        self.client = APIClient()

        # Criar usuário de teste com modelo personalizado
        User = get_user_model()
        self.user = User.objects.create_user(
            username="testuser",
            email="test@example.com",
            password="testpass123",
            first_name="Test",
            last_name="User",
            role="health_prof",
        )

        # Criar estudante de teste com campos corretos
        self.student = Student.objects.create(
            name="João Silva",
            cgm="1234567890",
            dob=date(2000, 1, 1),
            gender="M",
            guardian="Maria Silva",
            guardian_cpf="98765432100",
            address="Rua Teste, 123",
            cep="12345678",
            city="São Paulo",
            state="SP",
            created_by=self.user,
            updated_by=self.user,
        )

        # Criar entrada médica de teste
        self.medical_entry = MedicalEntry.objects.create(
            student=self.student,
            healthpro=self.user,
            description="Consulta de rotina",
            entry_date=timezone.now(),
        )

    def test_student_interval_report_without_dates(self):
        """Testa relatório de estudante sem datas (mês atual)"""
        self.client.force_authenticate(user=self.user)

        with patch("reports.views.MedicalEntry.objects.filter") as mock_filter:
            mock_filter.return_value.order_by.return_value = [self.medical_entry]

            response = self.client.get(
                f"/api/reports/medical-entries/interval/{self.student.pk}/"
            )

            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertEqual(
                response["Content-Type"],
                "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            )

    def test_student_interval_report_with_valid_dates(self):
        """Testa relatório de estudante com datas válidas"""
        self.client.force_authenticate(user=self.user)

        with patch("reports.views.MedicalEntry.objects.filter") as mock_filter:
            mock_filter.return_value.order_by.return_value = [self.medical_entry]

            response = self.client.get(
                f"/api/reports/medical-entries/interval/{self.student.pk}/?start_date=2023-01-01&end_date=2023-12-31"
            )

            self.assertEqual(response.status_code, status.HTTP_200_OK)
            mock_filter.assert_called_once()

    def test_student_interval_report_with_invalid_dates(self):
        """Testa relatório de estudante com datas inválidas"""
        self.client.force_authenticate(user=self.user)

        response = self.client.get(
            f"/api/reports/medical-entries/interval/{self.student.pk}/?start_date=invalid&end_date=invalid"
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(
            response.data["detail"], "Invalid date format. Use YYYY-MM-DD."
        )

    def test_student_interval_report_nonexistent_student(self):
        """Testa relatório para estudante inexistente"""
        self.client.force_authenticate(user=self.user)

        # Usar um UUID válido mas inexistente
        fake_uuid = "12345678-1234-5678-1234-567812345678"
        response = self.client.get(
            f"/api/reports/medical-entries/interval/{fake_uuid}/"
        )

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_student_interval_report_creates_log(self):
        """Testa se o relatório de estudante cria um log"""
        self.client.force_authenticate(user=self.user)

        with patch("reports.views.MedicalEntry.objects.filter") as mock_filter:
            mock_filter.return_value.order_by.return_value = []

            initial_log_count = ReportLog.objects.count()
            response = self.client.get(
                f"/api/reports/medical-entries/interval/{self.student.pk}/"
            )

            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.assertEqual(ReportLog.objects.count(), initial_log_count + 1)

            log = ReportLog.objects.latest("date")
            self.assertEqual(log.user_id, self.user)
            self.assertEqual(
                log.report_type, ReportLog.ReportTypes.STUDENT_HISTORY_SPECIFIED_PERIOD
            )

    @patch("reports.views.Workbook")
    def test_student_interval_report_excel_generation(self, mock_workbook):
        """Testa a geração do arquivo Excel no relatório de estudante"""
        self.client.force_authenticate(user=self.user)

        # Mock do workbook
        mock_wb = Mock()
        mock_sheet = Mock()
        mock_wb.active = mock_sheet
        mock_workbook.return_value = mock_wb

        # Mock do buffer
        mock_buffer = Mock()
        mock_buffer.getvalue.return_value = b"excel_content"

        with (
            patch("reports.views.MedicalEntry.objects.filter") as mock_filter,
            patch("reports.views.io.BytesIO", return_value=mock_buffer),
        ):
            mock_filter.return_value.order_by.return_value = [self.medical_entry]

            self.client.get(f"/api/reports/medical-entries/interval/{self.student.pk}/")

            # Verificar se o workbook foi configurado corretamente
            self.assertEqual(mock_sheet.title, f"Relatório - {self.student.name}")
            mock_sheet.append.assert_called()
            mock_wb.save.assert_called_once_with(mock_buffer)

    def test_student_interval_report_filename_generation(self):
        """Testa a geração do nome do arquivo no relatório de estudante"""
        self.client.force_authenticate(user=self.user)

        with patch("reports.views.MedicalEntry.objects.filter") as mock_filter:
            mock_filter.return_value.order_by.return_value = []

            response = self.client.get(
                f"/api/reports/medical-entries/interval/{self.student.pk}/?start_date=2023-01-01&end_date=2023-12-31"
            )

            self.assertEqual(response.status_code, status.HTTP_200_OK)
            content_disposition = response["Content-Disposition"]
            self.assertIn(
                "relatorio_João Silva_2023-01-01_2023-12-31.xlsx", content_disposition
            )

    def test_student_interval_report_unauthenticated(self):
        """Testa acesso não autenticado ao relatório de estudante"""
        response = self.client.get(
            f"/api/reports/medical-entries/interval/{self.student.pk}/"
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class ReportIntegrationTestCase(APITestCase):
    """Testes de integração para as views de relatórios"""

    def setUp(self):
        self.client = APIClient()

        # Criar usuário de teste com modelo personalizado
        User = get_user_model()
        self.user = User.objects.create_user(
            username="testuser",
            email="test@example.com",
            password="testpass123",
            first_name="Test",
            last_name="User",
            role="health_prof",
        )

        # Criar estudante de teste com campos corretos
        self.student = Student.objects.create(
            name="João Silva",
            cgm="1234567890",
            dob=date(2000, 1, 1),
            gender="M",
            guardian="Maria Silva",
            guardian_cpf="98765432100",
            address="Rua Teste, 123",
            cep="12345678",
            city="São Paulo",
            state="SP",
            created_by=self.user,
            updated_by=self.user,
        )

        # Criar múltiplas entradas médicas
        self.medical_entries = []
        for i in range(3):
            entry = MedicalEntry.objects.create(
                student=self.student,
                healthpro=self.user,
                description=f"Consulta {i + 1}",
                entry_date=timezone.now(),
            )
            self.medical_entries.append(entry)

    def test_monthly_report_with_real_data(self):
        """Testa relatório mensal com dados reais"""
        self.client.force_authenticate(user=self.user)

        response = self.client.get("/api/reports/medical-entries/monthly/")

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Verificar se o conteúdo é um arquivo Excel válido
        content = response.content
        self.assertGreater(len(content), 0)

        # Verificar headers HTTP
        self.assertEqual(
            response["Content-Type"],
            "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        )
        self.assertIn("attachment", response["Content-Disposition"])

    def test_student_interval_report_with_real_data(self):
        """Testa relatório de estudante com dados reais"""
        self.client.force_authenticate(user=self.user)

        response = self.client.get(
            f"/api/reports/medical-entries/interval/{self.student.pk}/"
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Verificar se o conteúdo é um arquivo Excel válido
        content = response.content
        self.assertGreater(len(content), 0)

        # Verificar headers HTTP
        self.assertEqual(
            response["Content-Type"],
            "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        )
        self.assertIn("attachment", response["Content-Disposition"])

    def test_report_logs_creation(self):
        """Testa se os logs de relatório são criados corretamente"""
        self.client.force_authenticate(user=self.user)

        initial_count = ReportLog.objects.count()

        # Gerar relatório mensal
        self.client.get("/api/reports/medical-entries/monthly/")

        # Gerar relatório de estudante
        self.client.get(f"/api/reports/medical-entries/interval/{self.student.pk}/")

        final_count = ReportLog.objects.count()
        self.assertEqual(final_count, initial_count + 2)

        # Verificar tipos de relatório
        logs = ReportLog.objects.order_by("-date")[:2]
        report_types = [log.report_type for log in logs]

        self.assertIn(ReportLog.ReportTypes.GENERAL_MONTHLY, report_types)
        self.assertIn(
            ReportLog.ReportTypes.STUDENT_HISTORY_SPECIFIED_PERIOD, report_types
        )


class ReportViewsEdgeCasesTestCase(APITestCase):
    """Testes para casos extremos das views de relatórios"""

    def setUp(self):
        self.client = APIClient()

        # Criar usuário de teste com modelo personalizado
        User = get_user_model()
        self.user = User.objects.create_user(
            username="testuser",
            email="test@example.com",
            password="testpass123",
            first_name="Test",
            last_name="User",
            role="health_prof",
        )

    def test_monthly_report_no_entries(self):
        """Testa relatório mensal sem entradas"""
        self.client.force_authenticate(user=self.user)

        response = self.client.get("/api/reports/medical-entries/monthly/")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Deve retornar um arquivo Excel mesmo sem dados
        self.assertGreater(len(response.content), 0)

    def test_student_report_no_entries(self):
        """Testa relatório de estudante sem entradas"""
        self.client.force_authenticate(user=self.user)

        # Criar estudante sem entradas médicas
        student = Student.objects.create(
            name="Maria Santos",
            cgm="1111111111",
            dob=date(2000, 1, 1),
            gender="F",
            guardian="José Santos",
            guardian_cpf="22222222222",
            address="Rua Teste, 456",
            cep="87654321",
            city="Rio de Janeiro",
            state="RJ",
            created_by=self.user,
            updated_by=self.user,
        )

        response = self.client.get(
            f"/api/reports/medical-entries/interval/{student.pk}/"
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Deve retornar um arquivo Excel mesmo sem dados
        self.assertGreater(len(response.content), 0)

    def test_monthly_report_future_date(self):
        """Testa relatório mensal para data futura"""
        self.client.force_authenticate(user=self.user)

        response = self.client.get(
            "/api/reports/medical-entries/monthly/?year=2030&month=12"
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Deve retornar um arquivo Excel mesmo para data futura
        self.assertGreater(len(response.content), 0)

    def test_student_report_invalid_date_range(self):
        """Testa relatório de estudante com range de datas inválido"""
        self.client.force_authenticate(user=self.user)

        student = Student.objects.create(
            name="Pedro Lima",
            cgm="3333333333",
            dob=date(2000, 1, 1),
            gender="M",
            guardian="Ana Lima",
            guardian_cpf="44444444444",
            address="Rua Teste, 789",
            cep="11111111",
            city="Belo Horizonte",
            state="MG",
            created_by=self.user,
            updated_by=self.user,
        )

        # Data de fim anterior à data de início
        response = self.client.get(
            f"/api/reports/medical-entries/interval/{student.pk}/?start_date=2023-12-31&end_date=2023-01-01"
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Deve processar mesmo com range inválido
        self.assertGreater(len(response.content), 0)
