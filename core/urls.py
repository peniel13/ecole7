# core/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('profile/', views.user_profile, name='user_profile'),
    path('teacher/<int:teacher_id>/dashboard/', views.teacher_dashboard, name='teacher_dashboard'),
    path('student/dashboard/<int:student_id>/', views.student_dashboard, name='student_dashboard'),
    path('class/<int:class_id>/', views.class_detail, name='class_detail'),
    path('signup/', views.signup, name='signup'),
    path('signin/', views.signin, name='signin'),
    path('signout/', views.signout, name='signout'),
    path('assign_classes_to_teachers/', views.assign_classes_to_teachers, name='assign_classes_to_teachers'),
    path('assign_classes_to_students/', views.assign_classes_to_students, name='assign_classes_to_students'),
    path('make_declaration/<int:student_id>/', views.make_declaration, name='make_declaration'),
    path('student/<int:student_id>/payment/', views.declare_payment, name='payment_form'),
    path('student/<int:student_id>/behavior/', views.declare_behavior, name='behavior_form'),
    path('student/<int:student_id>/note/', views.declare_note, name='note_form'),
    path('student/<int:student_id>/convocation/', views.declare_convocation, name='convocation_form'),
    path('student/<int:student_id>/attendance/', views.attendance_form, name='attendance_form'),
    path('userssuccess/<int:student_id>/', views.success_view, name='success_view'),
    path('usersstudent/dashboard/<int:student_id>/', views.student_dashboard, name='student_dashboard'),
    path('usersstudent/<int:student_id>/payments/', views.payment_list, name='payment_list'),
    path('usersstudent/<int:student_id>/behaviors/', views.behavior_list, name='behavior_list'),
    path('usersstudent/<int:student_id>/notes/', views.note_list, name='note_list'),
    path('student/<int:student_id>/convocations/', views.convocation_list, name='convocation_list'),
    path('usersstudent/<int:student_id>/attendances/', views.attendance_list, name='attendance_list'),
    path('usersstudent/<int:student_id>/update_attendance/', views.update_attendance, name='update_attendance'),
    path('controle/', views.controle, name='controle'),
    path('usersstudent/<int:student_id>/autres-frais/', views.autres_frais_list, name='autres_frais_list'),  # Liste des autres frais
    path('student/<int:student_id>/declare-autres-frais/', views.declare_autres_frais, name='declare_autres_frais'),  # Déclaration de nouveaux frais
]          