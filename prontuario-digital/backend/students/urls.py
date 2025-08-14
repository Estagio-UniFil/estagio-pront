from django.urls import path
from students import views

urlpatterns = [
    path("api/students/", views.student_list, name="student_list"),
    path("api/students/<uuid:pk>/", views.student_detail, name="student_detail"),
    path(
        "api/students/inactive/",
        views.inactive_student_list,
        name="inactive_student_list",
    ),
    path(
        "api/students/<uuid:pk>/restore/",
        views.restore_inactive_student,
        name="restore_inactive_student",
    ),
]
