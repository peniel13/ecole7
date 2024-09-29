from django.urls import path
from .import views

urlpatterns= [
    path('',views.index, name= 'index'),
    path('contact/', views.contact, name='contact'),
    path('apropos/', views.apropos, name='apropos'),  # Page à propos
    path('info/', views.info, name='info'),  # Page d'infos
    path('preinscription/', views.preinscription, name='preinscription'),  # Page de préinscription
    path('blog/<int:blog_id>/', views.blog_detail, name='blog_detail'),
    path('paye-en-ligne/', views.payment, name='paye_en_ligne'),
]

    
