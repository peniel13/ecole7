from django.shortcuts import render,get_object_or_404
from django.contrib import messages
from .forms import PaymentForm
from django.core.paginator import Paginator
from base.models import Contact, Preinscription,BlogInfo,Payment
import string  

# Create your views here.

def index(request):
    blogs = BlogInfo.objects.order_by('-created_at')[:3]
    return render (request, "base/index.html", {'blogs': blogs})

punc = string.punctuation  
def contact(request):
    # return HttpResponse('contact')
    if request.method=="POST":
        print('post')
        name = request.POST['name']
        email = request.POST['email']
        number = request.POST['number']
        content = request.POST['content']
        print(name,email,content,number)
        if len(name) >1 and len(name) < 30:
            pass
        else:
            messages.error(request,'length of Name should be greater than 2 and less than 30')
            return render(request,'base/contact.html')

        if len(email) >1 and len(email) < 30:
            pass
        else:
            messages.error(request,'email is not correct try again!!')
            return render(request,'base/contact.html')
        print(len(number))
        if len(number) > 9 and len(number) < 13:
            pass
        else:
            messages.error(request,'number not correct try again!!')
            return render(request,'base/contact.html')
        ins = Contact(name=name,email=email,content=content,number=number)
        ins.save()
        messages.success(request,'Thank You for contacting me!! Your message has been saved ')
        print('data has been saved to database')
    else:
        print('not post')
    return render(request,'base/contact.html')

def apropos(request):
    return render(request, 'base/apropos.html')

def info(request):
    blogs = BlogInfo.objects.all()
    paginator = Paginator(blogs, 5)  # 5 blogs par page
    page_number = request.GET.get('page')
    blogs = paginator.get_page(page_number)
    return render(request, 'base/infoblog.html', {'blogs': blogs})

def preinscription(request):
    if request.method == "POST":
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']
        description = request.POST['description']
        document = request.FILES.get('document')  # Pour récupérer le fichier

        # Ajoute ici des validations si nécessaire
        if len(first_name) < 2 or len(first_name) > 30:
            messages.error(request, 'Le prénom doit avoir entre 2 et 30 caractères.')
            return render(request, 'base/preinscription.html')

        if len(last_name) < 2 or len(last_name) > 30:
            messages.error(request, 'Le nom de famille doit avoir entre 2 et 30 caractères.')
            return render(request, 'base/preinscription.html')

        # Ajoute d'autres validations si nécessaire ici

        # Enregistrement dans la base de données
        ins = Preinscription(first_name=first_name, last_name=last_name, email=email, description=description, document=document)
        ins.save()
        messages.success(request, 'Merci pour votre préinscription ! Votre message a été enregistré.')
        return render(request, 'base/preinscription.html')  # Redirige ou retourne la même page

    # Si la méthode n'est pas POST, retourne le formulaire vide
    return render(request, 'base/preinscription.html')

def blog_detail(request, blog_id):
    blog = get_object_or_404(BlogInfo, id=blog_id)
    blogs = BlogInfo.objects.exclude(id=blog_id)  # Exclure le blog actuel
    return render(request, 'base/blog_detail.html', {'blog': blog, 'blogs': blogs})


from django.contrib import messages
from .forms import PaymentForm  # Assurez-vous d'importer votre formulaire

def payment(request):
    if request.method == "POST":
        # Récupération des données du formulaire
        transaction_id = request.POST.get('transaction_id')
        transaction_number = request.POST.get('transaction_number')

        # Ajoutez ici des validations si nécessaire
        if not transaction_id or not transaction_number:
            messages.error(request, 'Veuillez remplir tous les champs.')
            return render(request, 'base/payment.html', {'form': PaymentForm()})

        # Enregistrement dans la base de données ou traitement du paiement
        # Assurez-vous de créer une logique pour sauvegarder le paiement
        # Par exemple :
        # payment_instance = Payment(transaction_id=transaction_id, transaction_number=transaction_number)
        # payment_instance.save()

        messages.success(request, 'Votre paiement a été effectué avec succès !')
        return render(request, 'base/payment.html', {'form': PaymentForm()})

    # Si la méthode n'est pas POST, retourne le formulaire vide
    return render(request, 'base/payment.html', {'form': PaymentForm()})


