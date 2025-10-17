from django.urls import path
from medicalentry import views

urlpatterns = [
    path("api/medical-entry/", views.medical_entry_list, name="medical_entry_list"),
    path(
        "api/medical-entry/<int:pk>/",
        views.medical_entry_detail,
        name="medical_entry_detail",
    ),
    path(
        "api/medical-entry/student/<uuid:student_id>/",
        views.medical_entry_by_student,
        name="medical_entry_by_student",
    ),
]
