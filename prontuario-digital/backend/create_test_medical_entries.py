import os
import django
from datetime import datetime, timedelta
import random

# Configura o ambiente Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "medicalrecord.settings")
django.setup()

from medicalentry.models import MedicalEntry
from students.models import Student
from authentication.models import User


def create_test_medical_entries():
    """
    Cria entradas médicas de teste com IDs específicos para testar o sistema de filtros.

    Usa:
    - Estudante: e90dd50a-a471-4c5a-9489-12485719eaf3
    - Fisioterapeuta: 8f174b26-686d-42fb-9d87-e1f7bf0c7200
    - Psicólogo: 8f174b26-686d-42fb-9d87-e1f7bf0c7200
    """

    # IDs específicos fornecidos
    STUDENT_ID = "e90dd50a-a471-4c5a-9489-12485719eaf3"
    PHYSIOTHERAPIST_ID = "8f174b26-686d-42fb-9d87-e1f7bf0c7200"
    PSYCHOLOGIST_ID = "8f174b26-686d-42fb-9d87-e1f7bf0c7200"

    try:
        # Buscar o estudante
        student = Student.objects.get(id=STUDENT_ID)
        print(f"Estudante encontrado: {student}")

        # Buscar os profissionais
        physiotherapist = User.objects.get(id=PHYSIOTHERAPIST_ID)
        psychologist = User.objects.get(id=PSYCHOLOGIST_ID)

        print(f"Fisioterapeuta encontrado: {physiotherapist}")
        print(f"Psicólogo encontrado: {psychologist}")

        # Verificar se têm health_profile
        if hasattr(physiotherapist, "health_profile"):
            print(
                f"Especialidade do fisioterapeuta: {physiotherapist.health_profile.specialty}"
            )
        else:
            print("AVISO: Fisioterapeuta não possui health_profile")

        if hasattr(psychologist, "health_profile"):
            print(
                f"Especialidade do psicólogo: {psychologist.health_profile.specialty}"
            )
        else:
            print("AVISO: Psicólogo não possui health_profile")

    except Student.DoesNotExist:
        print(f"ERRO: Estudante com ID {STUDENT_ID} não encontrado")
        return
    except User.DoesNotExist as e:
        print(f"ERRO: Profissional não encontrado: {e}")
        return

    # Dados para entradas de fisioterapia
    physiotherapy_entries = [
        {
            "description": "Avaliação inicial - Dor lombar crônica",
            "notes": "Paciente relata dor há 6 meses. Limitação de movimento. Indicado fortalecimento muscular.",
        },
        {
            "description": "Sessão de fortalecimento muscular",
            "notes": "Exercícios para core e glúteos. Paciente apresentou boa evolução na amplitude de movimento.",
        },
        {
            "description": "Terapia manual - Mobilização articular",
            "notes": "Técnicas de mobilização para coluna lombar. Redução significativa da dor relatada.",
        },
        {
            "description": "Exercícios funcionais e propriocepção",
            "notes": "Trabalho de equilíbrio e coordenação. Paciente demonstra melhora na estabilidade postural.",
        },
        {
            "description": "Reavaliação - Progresso do tratamento",
            "notes": "Melhora de 70% no quadro álgico. Amplitude de movimento normalizada. Alta programada.",
        },
    ]

    # Dados para entradas de psicologia
    psychology_entries = [
        {
            "description": "Primeira consulta - Avaliação psicológica",
            "notes": "Paciente apresenta sintomas de ansiedade generalizada. Histórico de estresse acadêmico.",
        },
        {
            "description": "Sessão de terapia cognitivo-comportamental",
            "notes": "Trabalho com técnicas de reestruturação cognitiva. Identificação de pensamentos disfuncionais.",
        },
        {
            "description": "Técnicas de relaxamento e mindfulness",
            "notes": "Ensino de técnicas de respiração e relaxamento muscular progressivo. Boa adesão do paciente.",
        },
        {
            "description": "Terapia de exposição gradual",
            "notes": "Trabalho com situações que geram ansiedade. Hierarquia de exposição estabelecida.",
        },
        {
            "description": "Sessão de follow-up",
            "notes": "Paciente relata redução significativa dos sintomas ansiosos. Estratégias de enfrentamento consolidadas.",
        },
        {
            "description": "Avaliação de progresso terapêutico",
            "notes": "Melhora substancial no quadro. Paciente demonstra maior autoconfiança e controle emocional.",
        },
    ]

    # Lista para armazenar todas as entradas
    new_entries = []

    # Data base para as entradas (últimos 60 dias)
    base_date = datetime.now() - timedelta(days=60)

    # Criar entradas de fisioterapia
    print("\nCriando entradas de fisioterapia...")
    for i, entry_data in enumerate(physiotherapy_entries):
        # Distribuir as entradas ao longo do tempo
        entry_date = base_date + timedelta(
            days=random.randint(0, 30),
            hours=random.randint(8, 17),
            minutes=random.randint(0, 59),
        )

        entry = MedicalEntry(
            student=student,
            healthpro=physiotherapist,
            description=entry_data["description"],
            notes=entry_data["notes"],
            entry_date=entry_date,
        )
        new_entries.append(entry)
        print(f"  - {entry_data['description']}")

    # Criar entradas de psicologia
    print("\nCriando entradas de psicologia...")
    for i, entry_data in enumerate(psychology_entries):
        # Distribuir as entradas ao longo do tempo (mais recentes)
        entry_date = base_date + timedelta(
            days=random.randint(15, 45),
            hours=random.randint(8, 17),
            minutes=random.randint(0, 59),
        )

        entry = MedicalEntry(
            student=student,
            healthpro=psychologist,
            description=entry_data["description"],
            notes=entry_data["notes"],
            entry_date=entry_date,
        )
        new_entries.append(entry)
        print(f"  - {entry_data['description']}")

    # Salvar todas as entradas no banco
    try:
        MedicalEntry.objects.bulk_create(new_entries)
        print(f"\n✅ SUCESSO: {len(new_entries)} entradas médicas criadas!")
        print(f"   - {len(physiotherapy_entries)} entradas de fisioterapia")
        print(f"   - {len(psychology_entries)} entradas de psicologia")
        print(f"   - Todas para o estudante: {student}")

        # Verificar se as entradas foram criadas corretamente
        total_entries = MedicalEntry.objects.filter(
            student=student, deleted=False
        ).count()
        physio_entries = MedicalEntry.objects.filter(
            student=student, healthpro=physiotherapist, deleted=False
        ).count()
        psych_entries = MedicalEntry.objects.filter(
            student=student, healthpro=psychologist, deleted=False
        ).count()

        print(f"\n📊 VERIFICAÇÃO:")
        print(f"   - Total de entradas do estudante: {total_entries}")
        print(f"   - Entradas do fisioterapeuta: {physio_entries}")
        print(f"   - Entradas do psicólogo: {psych_entries}")

    except Exception as e:
        print(f"\n❌ ERRO ao salvar entradas: {e}")


def clean_test_entries():
    """
    Remove todas as entradas de teste criadas anteriormente (opcional)
    """
    STUDENT_ID = "e90dd50a-a471-4c5a-9489-12485719eaf3"

    try:
        student = Student.objects.get(id=STUDENT_ID)
        deleted_count = MedicalEntry.objects.filter(student=student).delete()[0]
        print(f"🗑️  {deleted_count} entradas removidas para o estudante {student}")
    except Student.DoesNotExist:
        print(f"Estudante com ID {STUDENT_ID} não encontrado")


if __name__ == "__main__":
    print("🏥 Script de Criação de Entradas Médicas de Teste")
    print("=" * 50)

    # Descomente a linha abaixo se quiser limpar entradas anteriores
    # clean_test_entries()

    # Criar as novas entradas de teste
    create_test_medical_entries()

    print("\n✨ Script executado com sucesso!")
