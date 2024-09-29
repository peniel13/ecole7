from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.conf import settings
from django.utils import timezone
import datetime


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, **extra_fields)

class CustomUser(AbstractBaseUser, PermissionsMixin):
    ROLE_CHOICES = [
        ('student', 'Student'),
        ('teacher', 'Teacher'),
        ('admin', 'Admin'),
    ]

    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=30, blank=True)
    last_name = models.CharField(max_length=30, blank=True)
    profile_pic = models.ImageField(upload_to="p_img", blank=True, null=True)
    address = models.CharField(max_length=50, blank=True, null=True)
    phone = models.CharField(max_length=11, blank=True, null=True)
    role = models.CharField(max_length=50, choices=ROLE_CHOICES)
    bio = models.TextField(blank=True, null=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    # Pour les professeurs, plusieurs classes
    assigned_classes = models.ManyToManyField('Class', blank=True, related_name='assigned_teachers')

    # Pour les élèves, une seule classe
    student_class = models.ForeignKey('Class', null=True, blank=True, on_delete=models.SET_NULL, related_name='students')

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    objects = CustomUserManager()

    def __str__(self):
        return self.email



class Class(models.Model):
    name = models.CharField(max_length=100)
    year = models.CharField(max_length=10)
    description = models.TextField()
    assigned = models.BooleanField(default=False)  # Indique si la classe est attribuée

    def __str__(self):
        return self.name


class StudentClass(models.Model):
    student = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    student_class = models.ForeignKey(Class, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('student', 'student_class')
        
class Payment(models.Model):
    MONTH_CHOICES = [ 
        ('september', 'September'),
        ('october', 'October'),
        ('november', 'November'),
        ('december', 'December'),
        ('january', 'January'),
        ('february', 'February'),
        ('march', 'March'),
        ('april', 'April'),
        ('may', 'May'),
        ('june', 'June'),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True)
    reason = models.CharField(max_length=100)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    month = models.CharField(max_length=10, choices=MONTH_CHOICES)
    class_assigned = models.ForeignKey(Class, on_delete=models.CASCADE, related_name='payments', null=True)   # Nouveau champ

    def __str__(self):
        return f"{self.user.email} - {self.reason} - {self.amount} - {self.month}"

class Behavior(models.Model):
    LEVEL_CHOICES = [
        ('bad', 'Mauvais'),
        ('average', 'Moyen'),
        ('good', 'Bon'),
    ]

    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True)
    commentaire = models.TextField()  # Nouveau champ pour le commentaire
    level = models.CharField(max_length=10, choices=LEVEL_CHOICES)
    periode = models.CharField(max_length=100, null=True)   # Nouveau champ pour la période


class Note(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True)
    epreuve = models.CharField(max_length=100)
    date_epreuve = models.DateField(default=datetime.date.today)  # Nouveau champ pour la date de l'épreuve
    note = models.CharField(max_length=10)  # Modifié pour "note"

class AutresFrais(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True)  # Ajout du champ user
    motif = models.CharField(max_length=100)  # Champ pour le motif
    date_frais = models.DateField(default=datetime.date.today)  # Champ pour la date de frais
    montant = models.DecimalField(max_digits=10, decimal_places=2)  # Champ pour le montant


 
class Attendance(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True)
    absences = models.IntegerField(default=0)
    presences = models.IntegerField(default=0)

    class Meta:
        unique_together = ('user',)  # Assurez-vous qu'il n'y a qu'une seule entrée par élève

    def __str__(self):
        return f"{self.user} - Absences: {self.absences}, Presences: {self.presences}"

class Convocation(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True)  # Associe la convocation à un utilisateur
    titre = models.CharField(max_length=100)  # Champ pour le titre
    raison = models.TextField()  # Champ pour la raison de convocation
    statut = models.CharField(max_length=50)  # Champ pour le statut de la personne convoquée

    def __str__(self):
        return self.titre


class TeacherClassAssignment(models.Model):
    teacher = models.ForeignKey(CustomUser, on_delete=models.CASCADE, limit_choices_to={'role': 'teacher'})
    class_assigned = models.ForeignKey(Class, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('teacher', 'class_assigned')

    def __str__(self):
        return f"{self.teacher.email} -> {self.class_assigned.name}"

class StudentClassAssignment(models.Model):
    student = models.ForeignKey(CustomUser, on_delete=models.CASCADE, limit_choices_to={'role': 'student'})
    student_class = models.ForeignKey(Class, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.student.email} -> {self.student_class.name}"

 # Retourne le titre lorsque l'objet est affiché
    






