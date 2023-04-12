from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Evento
from django.urls import reverse
from django.contrib import messages
from django.contrib.messages import constants


@login_required  # exigir login
def novo_evento(request):
    if request.method == "GET":
        return render(request, 'novo_evento.html')
    elif request.method == "POST":
        # busca as informações que estão vindo do HTML
        nome = request.POST.get('nome')
        descricao = request.POST.get('descricao')
        data_inicio = request.POST.get('data_inicio')
        data_termino = request.POST.get('data_termino')
        carga_horaria = request.POST.get('carga_horaria')

        cor_principal = request.POST.get('cor_principal')
        cor_secundaria = request.POST.get('cor_secundaria')
        cor_fundo = request.POST.get('cor_fundo')

        logo = request.FILES.get('logo')

        evento = Evento(
            criador=request.user,  # usuário logado
            nome=nome,
            descricao=descricao,
            data_inicio=data_inicio,
            data_termino=data_termino,
            carga_horaria=carga_horaria,
            cor_principal=cor_principal,
            cor_secundaria=cor_secundaria,
            cor_fundo=cor_fundo,
            logo=logo,
        )

        evento.save()

        messages.add_message(request, constants.SUCCESS,
                             'Evento cadastrado com sucesso')
        return redirect(reverse('novo_evento'))


def gerenciar_evento(request):
    if request.method == "GET":
        nome = request.GET.get('nome')
        # filtra o que vc quer buscar, nesse caso os eventos do usuário logado
        eventos = Evento.objects.filter(criador=request.user)
        if nome:
            eventos = eventos.filter(nome__contains=nome)
        return render(request, 'gerenciar_evento.html', {'eventos': eventos})


@login_required
def inscrever_evento(request, id):
    # Validar login
    evento = get_object_or_404(Evento, id=id)  # pega o objeto ou passa o erro
    if request.method == "GET":
        return render(request, 'inscrever_evento.html', {'evento': evento})
    elif request.method == "POST":

        evento.participantes.add(request.user)
        evento.save()

        messages.add_message(request, constants.SUCCESS,
                             'Inscrição realizada com sucesso.')
        return redirect(reverse('inscrever_evento', kwargs={'id': id}))
