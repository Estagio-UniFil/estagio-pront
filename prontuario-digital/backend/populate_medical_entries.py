import os
import django
from datetime import date, timedelta
import random

# Configura o ambiente Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "medicalrecord.settings")
django.setup()

from medicalentry.models import MedicalEntry
from students.models import Student
from authentication.models import User, HealthProfile


def create_medical_entries_batch(num_entries=100, student_id=None):
    """
    Cria um lote de MedicalEntry no banco de dados para fins de teste.

    Args:
        num_entries (int): O número de entradas a serem criadas.
        student_id (str, optional): O ID do estudante para o qual as entradas serão criadas.
                                     Se None, um estudante aleatório será escolhido.
    """

    # Busca todos os estudantes e profissionais de saúde
    students = list(Student.objects.all())
    health_profs = list(User.objects.filter(role="health_prof"))

    if not students or not health_profs:
        print(
            "Erro: Nenhum estudante ou profissional de saúde encontrado. Certifique-se de que existem no banco de dados."
        )
        return

    # Se um student_id específico for fornecido, usa-o. Caso contrário, escolhe um aleatoriamente.
    if student_id:
        try:
            student_to_use = Student.objects.get(id=student_id)
        except Student.DoesNotExist:
            print(f"Erro: Estudante com ID {student_id} não encontrado.")
            return
    else:
        student_to_use = random.choice(students)

    new_entries = []
    base_date = date.today() - timedelta(days=30)

    specialties = [
        "psychologist",
        "physiotherapist",
        "social_worker",
        "speech_therapist",
    ]

    for i in range(num_entries):
        # Escolhe um profissional de saúde aleatoriamente
        healthpro = random.choice(health_profs)

        # Garante que a especialidade do profissional seja válida para os dados
        try:
            specialty = healthpro.health_profile.specialty
        except HealthProfile.DoesNotExist:
            # Se o usuário não tiver HealthProfile, usa uma especialidade aleatória para o exemplo
            specialty = random.choice(specialties)

        # Dados da entrada médica
        description = f"Entrada de teste ({specialty}) - Descrição {i + 1}"
        notes = f"Notas adicionais para a entrada ({specialty}) {i + 1}"

        # Cria uma data de entrada aleatória
        entry_date = base_date + timedelta(
            days=random.randint(0, 29), hours=random.randint(0, 23)
        )

        # Cria uma instância do modelo MedicalEntry
        entry = MedicalEntry(
            student=student_to_use,
            healthpro=healthpro,
            description=description,
            notes=notes,
            entry_date=entry_date,
        )
        new_entries.append(entry)

    # Usa bulk_create para inserir todos os objetos de uma vez
    MedicalEntry.objects.bulk_create(new_entries)
    print(
        f"{num_entries} entradas médicas criadas com sucesso para o estudante '{student_to_use.name}'."
    )


if __name__ == "__main__":
    # Exemplo de uso: cria 50 entradas para um estudante com um ID específico
    # Substitua 'seu_id_de_estudante_aqui' pelo ID real do estudante
    # create_medical_entries_batch(num_entries=50, student_id="seu_id_de_estudante_aqui")

    # Exemplo de uso: cria 20 entradas para um estudante aleatório
    create_medical_entries_batch(num_entries=20)
