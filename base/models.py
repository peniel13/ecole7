from django.db import models
from django.utils import timezone

# Create your models here.


class BlogInfo(models.Model):
    title = models.CharField(max_length=200)  # Titre du blog
    content = models.TextField()                # Énoncé ou contenu
    description = models.TextField()            # Description du blog
    image = models.ImageField(upload_to='blog_images/')  # Champ pour l'image
    created_at = models.DateTimeField(default=timezone.now)  # Date de création

    def __str__(self):
        return self.title

class Contact(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=40)
    email = models.EmailField(max_length=40)
    content = models.TextField(max_length=400)
    number  = models.CharField(max_length=10)

    def __str__(self):
        return (self.name)

class Preinscription(models.Model):
    first_name = models.CharField(max_length=40)  # Nom à inscrire
    last_name = models.CharField(max_length=40)   # Postnom
    email = models.EmailField(max_length=40)       # Email
    description = models.TextField(max_length=400)  # Description
    document = models.FileField(upload_to='documents/')  # Champ pour télécharger un document

    def __str__(self):
        return f"{self.first_name} {self.last_name}"



class Payment(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=40)
    position = models.CharField(max_length=40)
    email = models.EmailField(max_length=40)
    phone = models.CharField(max_length=15)  # Adjust length as needed
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    device = models.CharField(max_length=30)
    transaction_id = models.CharField(max_length=30)
    transaction_number = models.CharField(max_length=30)
    description = models.TextField(max_length=400)

    def __str__(self):
        return f"{self.name} - {self.amount}"
