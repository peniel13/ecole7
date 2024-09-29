from django.contrib import admin
from .models import CustomUser, Class, Payment, Behavior, Note, Attendance,TeacherClassAssignment,StudentClassAssignment,AutresFrais,Convocation

@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('email', 'first_name', 'last_name', 'role', 'is_staff')
    search_fields = ('email', 'first_name', 'last_name')
    filter_horizontal = ('assigned_classes',)

@admin.register(Class)
class ClassAdmin(admin.ModelAdmin):
    list_display = ('name', 'year', 'description', 'assigned')
    search_fields = ('name', 'year')


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    # Retire 'user' de la liste d'affichage
    list_display = ('reason', 'amount', 'month')
    search_fields = ('reason',)

@admin.register(Note)
class NoteAdmin(admin.ModelAdmin):
    list_display = ('epreuve', 'date_epreuve', 'note')
    search_fields = ('epreuve',)

@admin.register(Behavior)
class BehaviorAdmin(admin.ModelAdmin):
    list_display = ('commentaire', 'level', 'periode')
    search_fields = ('commentaire',)

@admin.register(AutresFrais)
class AutresFraisAdmin(admin.ModelAdmin):
    list_display = ('motif', 'date_frais', 'montant')
    search_fields = ('motif',) 



@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    # Retire 'user' de la liste d'affichage
    list_display = ('absences', 'presences')
    search_fields = ('absences', 'presences')


@admin.register(Convocation)
class ConvocationAdmin(admin.ModelAdmin):
    list_display = ('titre', 'statut')
    search_fields = ('titre', 'raison')



@admin.register(TeacherClassAssignment)
class TeacherClassAssignmentAdmin(admin.ModelAdmin):
    list_display = ('teacher', 'class_assigned')
    list_filter = ('teacher', 'class_assigned')

@admin.register(StudentClassAssignment)
class StudentClassAssignmentAdmin(admin.ModelAdmin):
    list_display = ('student', 'student_class')
    list_filter = ('student_class', 'student')
    search_fields = ('student__email', 'student_class__name')

 # Ordre par date de création
