from django.shortcuts import render
from eventos.models import Certificado, Evento

# Create your views here.


def meus_certificados(request):
    certificados = Certificado.objects.filter(participante=request.user)
    return render(request, 'meus_certificados.html', {'certificados': certificados})


def meus_eventos(request):
    eventos = Evento.objects.filter(participantes=request.user)
    return render(request, 'meus_eventos.html', {'eventos': eventos})
