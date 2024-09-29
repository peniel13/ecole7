from django.contrib import admin
from .forms import BlogInfoForm, ContactForm,PreinscriptionForm,PaymentForm
from .models import BlogInfo, Contact,Preinscription,Payment

# Register your models here.


@admin.register(BlogInfo)
class BlogInfoAdmin(admin.ModelAdmin):
    form = BlogInfoForm  # Utiliser le formulaire personnalisé
    list_display = ('title', 'created_at')  # Champs à afficher dans la liste
    search_fields = ('title', 'description')  # Champs de recherche
    ordering = ('-created_at',)  # Ordre par date de création

@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    form = ContactForm  # Utiliser le formulaire personnalisé
    list_display = ('name', 'email', 'number')  # Champs à afficher dans la liste
    search_fields = ('name', 'email')  # Champs de recherche
    ordering = ('name',)

@admin.register(Preinscription)
class PreinscriptionAdmin(admin.ModelAdmin):
    form = PreinscriptionForm  # Utiliser le formulaire personnalisé
    list_display = ('first_name', 'last_name', 'email')  # Champs à afficher dans la liste
    search_fields = ('first_name', 'last_name', 'email')  # Champs de recherche
    ordering = ('first_name',) 

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    form = PaymentForm
    list_display = ('name', 'email', 'amount', 'transaction_id')
    search_fields = ('name', 'email', 'transaction_id')
    ordering = ('name',)