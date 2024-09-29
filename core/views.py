# core/views.py
from django.shortcuts import render, redirect, get_object_or_404
from .forms import PaymentForm, BehaviorForm, NoteForm, AttendanceForm,CustomUserForm,AutresFraisForm,ConvocationForm
from django.contrib.auth import authenticate, login, logout
from collections import defaultdict
from django.db.models import Count
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.admin.views.decorators import staff_member_required
from .forms import RegisterForm
from django.core.paginator import Paginator
from django.db.models import Sum
from .models import CustomUser, Class, Payment, Behavior, Note, Attendance,StudentClass,TeacherClassAssignment, StudentClassAssignment,AutresFrais,Convocation

def signup(request):
    form = RegisterForm(request=request)  # Passer le request ici
    if request.method == 'POST':
        form = RegisterForm(request.POST, request=request)  # Passer le request ici
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            messages.success(request, "Account created successfully")
            return redirect("signup")  # Rediriger vers une page appropriée
    context = {"form": form}
    return render(request, "core/signup.html", context)

def signin(request):
    if request.method == 'POST':
        email = request.POST.get("email")
        password = request.POST.get("password")

        user = authenticate(request, email=email, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, "Logged in successfully")
            return redirect('index')  # Redirection vers la page d'accueil ou une autre page appropriée
        else:
            messages.error(request, "Invalid email or password")
    
    context = {}
    return render(request, "core/login.html", context)

def signout(request):
    logout(request)
    return redirect("signin")  # Redirect to the sign-in page after logout


@login_required
def user_profile(request):
    user = request.user

    if request.method == 'POST':
        form = CustomUserForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, "Profile updated successfully.")
            return redirect('user_profile')
    else:
        form = CustomUserForm(instance=user)

    context = {
        'user': user,
        'form': form,
    }

    return render(request, 'core/user_profile.html', context)


@login_required
def teacher_dashboard(request, teacher_id):
    user = get_object_or_404(CustomUser, id=teacher_id, role='teacher')

    # Vérifiez si l'utilisateur est un enseignant ou un admin
    if request.user.role != 'teacher' and request.user.role != 'admin':
        return redirect('user_profile')

    assigned_classes = TeacherClassAssignment.objects.filter(teacher=user)

    return render(request, 'core/teacher_dashboard.html', {
        'assigned_classes': assigned_classes,
        'teacher': user
    })

@login_required
def student_dashboard(request, student_id):
    user = request.user
    student = get_object_or_404(CustomUser, id=student_id, role='student')

    # Vérifier si l'utilisateur est un enseignant, un admin ou l'élève lui-même
    if user.role not in ['teacher', 'admin'] and user != student:
        return redirect('user_profile')

    # Récupérer les classes assignées à l'élève
    student_classes = StudentClassAssignment.objects.filter(student=student)
    
    # Récupérer les informations personnelles de l'élève
    payments = Payment.objects.filter(user=student)
    behaviors = Behavior.objects.filter(user=student)
    notes = Note.objects.filter(user=student)
    attendances = Attendance.objects.filter(user=student)
    
    # Récupérer les autres frais associés à l'élève
    autres_frais = AutresFrais.objects.filter(user=student)
    convocations = Convocation.objects.filter(user=student)

    context = {
        'student': student,
        'student_classes': student_classes,
        'payments': payments,
        'behaviors': behaviors,
        'notes': notes,
        'attendances': attendances,
        'convocations': convocations,
        'autres_frais': autres_frais,  # Ajoutez ici les autres frais
    }

    return render(request, 'core/student_dashboard.html', context)




@login_required
def class_detail(request, class_id):
    user = request.user
    class_instance = get_object_or_404(Class, id=class_id)

    # Vérifier le rôle de l'utilisateur
    if user.role not in ['teacher', 'admin', 'student']:
        return redirect('user_profile')

    # Obtenir les élèves de la classe
    students = CustomUser.objects.filter(studentclassassignment__student_class=class_instance)

    # Pagination
    paginator = Paginator(students, 10)  # Affiche 10 élèves par page
    page_number = request.GET.get('page')
    students_paginated = paginator.get_page(page_number)

    # Statistiques des paiements
    total_students = students.count()

    # Montant total payé
    total_amount_paid = Payment.objects.filter(class_assigned=class_instance).aggregate(total=Sum('amount'))['total'] or 0

    # Paiements par mois
    payments_by_month = Payment.objects.filter(class_assigned=class_instance) \
        .values('month') \
        .annotate(monthly_total=Sum('amount')) \
        .order_by('month')

    # Paiements par élève
    payments_per_student = Payment.objects.filter(class_assigned=class_instance) \
        .values('user__first_name', 'user__last_name') \
        .annotate(payment_count=Count('id')) \
        .order_by('user__first_name')

    context = {
        'class_instance': class_instance,
        'students': students_paginated,
        'total_students': total_students,
        'total_amount_paid': total_amount_paid,
        'payments_by_month': payments_by_month,
        'payments_per_student': payments_per_student,
        'search_query': request.GET.get('search_query', ''),
    }

    return render(request, 'core/class_detail.html', context)






# @login_required
# def class_detail(request, class_id):
#     user = request.user
#     class_instance = get_object_or_404(Class, id=class_id)
    
#     if user.role != 'teacher' or not TeacherClassAssignment.objects.filter(teacher=user, class_assigned=class_instance).exists():
#         return redirect('user_profile')

#     # Liste des élèves assignés à cette classe
#     students = CustomUser.objects.filter(studentclassassignment__student_class=class_instance)

#     if request.method == 'POST':
#         student_id = request.POST.get('student_id')
#         student = get_object_or_404(CustomUser, id=student_id)
#         # Process declarations for the student here
#         return redirect('student_detail', student_id=student.id)

#     return render(request, 'core/class_detail.html', {
#         'class': class_instance,
#         'students': students
#     })


@staff_member_required
def assign_classes_to_teachers(request):
    if request.method == 'POST':
        teacher_ids = request.POST.getlist('teacher_ids')
        class_id = request.POST['class_id']
        class_instance = get_object_or_404(Class, id=class_id)

        # Clear previous assignments and create new ones
        TeacherClassAssignment.objects.filter(class_assigned=class_instance).delete()
        for teacher_id in teacher_ids:
            TeacherClassAssignment.objects.create(teacher_id=teacher_id, class_assigned=class_instance)

        messages.success(request, "Classes assigned to teachers successfully.")
        return redirect('assign_classes_to_teachers')

    # List all unassigned classes
    unassigned_classes = Class.objects.filter(teacherclassassignment__isnull=True).distinct()
    teachers = CustomUser.objects.filter(role='teacher')

    return render(request, 'core/assign_classes_to_teachers.html', {
        'unassigned_classes': unassigned_classes,
        'teachers': teachers
    })



@staff_member_required
def assign_classes_to_students(request):
    if request.method == 'POST':
        student_ids = request.POST.getlist('student_ids')  # Permet la sélection multiple
        class_id = request.POST.get('class_id')  # Utiliser get pour éviter une KeyError
        class_instance = get_object_or_404(Class, id=class_id)

        # Vérifiez s'il y a des IDs d'élèves sélectionnés
        if not student_ids:
            messages.error(request, "No students selected.")
            return redirect('assign_classes_to_students')

        # Supprimer les précédentes assignations pour cette classe
        StudentClassAssignment.objects.filter(student_class=class_instance).delete()

        # Créer de nouvelles assignations
        for student_id in student_ids:
            StudentClassAssignment.objects.create(student_id=student_id, student_class=class_instance)

        messages.success(request, "Classes assigned to students successfully.")
        return redirect('assign_classes_to_students')

    classes = Class.objects.all()
    students = CustomUser.objects.filter(role='student')

    return render(request, 'core/assign_classes_to_students.html', {
        'classes': classes,
        'students': students
    })



@login_required
def make_declaration(request, student_id):
    student = get_object_or_404(CustomUser, id=student_id, role='student')

    if request.method == 'POST':
        # Choisir quel formulaire utiliser en fonction de l'action
        if 'submit_payment' in request.POST:
            form = PaymentForm(request.POST)
            if form.is_valid():
                payment = form.save(commit=False)
                payment.user = student  # Assigne l'élève à la déclaration
                payment.save()
                return redirect('success_url')  # Remplace 'success_url' par l'URL appropriée
            
        elif 'submit_behavior' in request.POST:
            form = BehaviorForm(request.POST)
            if form.is_valid():
                behavior = form.save(commit=False)
                behavior.user = student
                behavior.save()
                return redirect('success_url')
        
        elif 'submit_note' in request.POST:
            form = NoteForm(request.POST)
            if form.is_valid():
                note = form.save(commit=False)
                note.user = student
                note.save()
                return redirect('success_url')
        
        elif 'submit_attendance' in request.POST:
            form = AttendanceForm(request.POST)
            if form.is_valid():
                attendance = form.save(commit=False)
                attendance.user = student
                attendance.save()
                return redirect('success_url')
    
    else:
        # Initialiser les formulaires avec l'utilisateur automatiquement assigné
        payment_form = PaymentForm(initial={'user': student})
        behavior_form = BehaviorForm(initial={'user': student})
        note_form = NoteForm(initial={'user': student})
        attendance_form = AttendanceForm(initial={'user': student})

    context = {
        'student': student,
        'payment_form': payment_form,
        'behavior_form': behavior_form,
        'note_form': note_form,
        'attendance_form': attendance_form
    }
    return render(request, 'core/make_declaration.html', context)


@login_required
def declare_payment(request, student_id):
    student = get_object_or_404(CustomUser, id=student_id)

    # Récupérer l'assignation de classe de l'élève
    student_class_assignment = get_object_or_404(StudentClassAssignment, student=student)

    if request.method == 'POST':
        form = PaymentForm(request.POST)
        if form.is_valid():
            payment = form.save(commit=False)
            payment.user = student
            payment.class_assigned = student_class_assignment.student_class  # Associer la classe
            payment.save()
            return redirect('success_view', student_id=student.id)
    else:
        form = PaymentForm(initial={'class_assigned': student_class_assignment.student_class})

    context = {
        'student': student,
        'form': form,
    }
    return render(request, 'core/payment_form.html', context)


def declare_behavior(request, student_id):
    student = get_object_or_404(CustomUser, id=student_id)
    
    if request.method == 'POST':
        form = BehaviorForm(request.POST)
        if form.is_valid():
            behavior = form.save(commit=False)
            behavior.user = student
            behavior.save()
            return redirect('success_view', student_id=student.id)

    else:
        form = BehaviorForm()

    context = {
        'student': student,
        'form': form,
    }
    return render(request, 'core/behavior_form.html', context)




def declare_note(request, student_id):
    student = get_object_or_404(CustomUser, id=student_id)
    
    if request.method == 'POST':
        form = NoteForm(request.POST)
        if form.is_valid():
            note = form.save(commit=False)
            note.user = student
            note.save()
            return redirect('success_view', student_id=student.id)

    else:
        form = NoteForm()

    context = {
        'student': student,
        'form': form,
    }
    return render(request, 'core/note_form.html', context)

@login_required
def declare_autres_frais(request, student_id):
    student = get_object_or_404(CustomUser, id=student_id)  # Récupération de l'étudiant

    if request.method == 'POST':
        form = AutresFraisForm(request.POST)
        if form.is_valid():
            autres_frais = form.save(commit=False)
            autres_frais.user = student  # Associer les frais à l'étudiant
            autres_frais.save()
            return redirect('success_view', student_id=student.id)  # Remplacez par la vue de redirection souhaitée
    else:
        form = AutresFraisForm()

    context = {
        'student': student,
        'form': form,
    }
    return render(request, 'core/autres_frais_form.html', context)


@login_required
def declare_convocation(request, student_id):
    student = get_object_or_404(CustomUser, id=student_id) # Récupération de l'utilisateur

    if request.method == 'POST':
        form = ConvocationForm(request.POST)
        if form.is_valid():
            convocation = form.save(commit=False)
            convocation.user = student  # Associer la convocation à l'utilisateur
            convocation.save()
            return redirect('success_view', student_id=student.id)  # Remplacez par la vue de redirection souhaitée
    else:
        form = ConvocationForm()

    context = {
        'user': student,
        'form': form,
    }
    return render(request, 'core/convocation_form.html', context)




@login_required
def attendance_form(request, student_id):
    student = get_object_or_404(CustomUser, id=student_id)

    # Récupérer ou créer l'enregistrement d'attendance
    attendance, created = Attendance.objects.get_or_create(user=student)

    if request.method == 'POST':
        # Mettre à jour les absences et présences
        attendance.absences = request.POST.get('absences', 0)
        attendance.presences = request.POST.get('presences', 0)
        attendance.save()
        
        messages.success(request, "Attendance updated successfully.")
        return redirect('attendance_list', student_id=student.id)

    return render(request, 'core/attendance_form.html', {'student': student, 'attendance': attendance})


def success_view(request, student_id):
    return render(request, 'core/success.html', {'student_id': student_id})


@login_required
def payment_list(request, student_id):
    student = get_object_or_404(CustomUser, id=student_id)
    payments = Payment.objects.filter(user=student)
    
    context = {
        'student': student,
        'payments': payments,
    }
    return render(request, 'core/payment_list.html', context)

@login_required
def behavior_list(request, student_id):
    student = get_object_or_404(CustomUser, id=student_id)
    behaviors = Behavior.objects.filter(user=student)
    
    context = {
        'student': student,
        'behaviors': behaviors,
    }
    return render(request, 'core/behavior_list.html', context)

@login_required
def note_list(request, student_id):
    student = get_object_or_404(CustomUser, id=student_id)
    notes = Note.objects.filter(user=student)
    
    context = {
        'student': student,
        'notes': notes,
    }
    return render(request, 'core/note_list.html', context)

@login_required
def autres_frais_list(request, student_id):
    student = get_object_or_404(CustomUser, id=student_id)  # Récupération de l'étudiant
    autres_frais = AutresFrais.objects.filter(user=student)  # Récupération des frais associés à l'étudiant

    context = {
        'student': student,
        'autres_frais': autres_frais,
    }
    return render(request, 'core/autres_frais_list.html', context)

@login_required
def convocation_list(request, student_id):
    student = get_object_or_404(CustomUser, id=student_id)  # Récupération de l'étudiant
    convocations = Convocation.objects.filter(user=student)  # Récupération des convocations associées à l'étudiant

    context = {
        'student': student,
        'convocations': convocations,
    }
    return render(request, 'core/convocation_list.html', context)


@login_required
def attendance_list(request, student_id):
    student = get_object_or_404(CustomUser, id=student_id)
    attendances = Attendance.objects.filter(user=student)
    
    context = {
        'student': student,
        'attendances': attendances,
    }
    return render(request, 'core/attendance_list.html', context)


def update_attendance(request, student_id):
    attendance = get_object_or_404(Attendance, user__id=student_id)  # Assurez-vous d'avoir une entrée existante

    if request.method == 'POST':
        form = AttendanceForm(request.POST, instance=attendance)
        if form.is_valid():
            form.save()
            return redirect('success_view')  # Redirigez vers la page de succès ou dashboard
    else:
        form = AttendanceForm(instance=attendance)

    context = {
        'form': form,
        'attendance': attendance,
    }
    return render(request, 'core/update_attendance.html', context)




@staff_member_required
def controle(request):
    if request.user.role != 'admin':
        return redirect('user_profile')

    # Récupérer les données nécessaires
    total_students = CustomUser.objects.filter(role='student').count()
    total_teachers = CustomUser.objects.filter(role='teacher').count()
    total_classes = Class.objects.count()

    # Compter le total d'élèves assignés
    total_assigned_students = StudentClassAssignment.objects.count()

    payments = Payment.objects.all()
    total_fees_collected = sum(payment.amount for payment in payments)

    # Comptabiliser le nombre de paiements par mois
    monthly_payments = defaultdict(int)
    for payment in payments:
        monthly_payments[payment.month] += 1

    # Créer un dictionnaire pour associer les mois aux paiements
    payment_count_by_month = {month[0]: monthly_payments[month[0]] for month in Payment.MONTH_CHOICES}

    # Comptabiliser le nombre de paiements par classe et par mois
    payments_by_class_and_month = defaultdict(lambda: defaultdict(int))
    for payment in payments:
        if payment.user.student_class:
            class_name = payment.user.student_class.name
            payments_by_class_and_month[class_name][payment.month] += 1

    classes = Class.objects.annotate(student_count=Count('studentclassassignment'))  # Compter les étudiants
    teachers = CustomUser.objects.filter(role='teacher')

    context = {
        'total_students': total_students,
        'total_teachers': total_teachers,
        'total_classes': total_classes,
        'total_assigned_students': total_assigned_students,
        'total_fees_collected': total_fees_collected,
        'payment_count_by_month': payment_count_by_month,
        'payments_by_class_and_month': payments_by_class_and_month,
        'classes': classes,
        'teachers': teachers,
    }

    return render(request, 'core/controle.html', context)




# @login_required
# def admin_dashboard(request):
#     if request.user.role != 'admin':
#         return redirect('user_profile')  # Rediriger si l'utilisateur n'est pas admin

#     # Récupérer les données nécessaires
#     total_students = CustomUser.objects.filter(role='student').count()
#     total_teachers = CustomUser.objects.filter(role='teacher').count()
#     total_classes = Class.objects.count()

#     payments = Payment.objects.all()
#     total_fees_collected = sum(payment.amount for payment in payments)
    
#     # Compter les étudiants en règle et non en règle par mois
#     monthly_payments = {}
#     for payment in payments:
#         month = payment.month
#         if month not in monthly_payments:
#             monthly_payments[month] = {'paid': 0, 'unpaid': 0}
#         if payment.user.is_active:  # Vérifier si l'élève est actif
#             monthly_payments[month]['paid'] += 1
#         else:
#             monthly_payments[month]['unpaid'] += 1

#     classes = Class.objects.all()

#     context = {
#         'total_students': total_students,
#         'total_teachers': total_teachers,
#         'total_classes': total_classes,
#         'total_fees_collected': total_fees_collected,
#         'monthly_payments': monthly_payments,
#         'classes': classes,
#     }

#     return render(request, 'core/admin_dashboard.html', context)







