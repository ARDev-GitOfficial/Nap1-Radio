import re

from django.contrib import messages
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.shortcuts import redirect, render

from .models import Musica, PedidoMusical


def index(request): return render(request, 'index.html')


def pedidos(request):
    musicas = Musica.objects.all()
    erro = ''

    if request.method == 'POST':
        nome = request.POST.get('nome_ouvinte', '').strip(); localidade = request.POST.get('localidade', '').strip()
        musica_id = request.POST.get('musica'); tipo = request.POST.get('tipo_contato')
        contato = request.POST.get('contato', '').strip()
        mensagem = request.POST.get('mensagem', '').strip()

        if not nome or not localidade or not musica_id or tipo not in ['telefone', 'email'] or not contato:
            erro = 'Preencha os campos obrigatórios.'
        elif not all(request.POST.get(campo) for campo in ['aceita_politica', 'confirma_dados', 'aceita_condicoes']):
            erro = 'Marque as três confirmações.'
        elif tipo == 'email':
            try:
                validate_email(contato)
            except ValidationError:
                erro = 'Digite um e-mail válido.'
        elif not re.fullmatch(r'[\d\s()+-]{8,20}', contato) or len(''.join(numero for numero in contato if numero.isdigit())) < 8:
            erro = 'Digite um telefone válido.'

        try:
            musica = Musica.objects.filter(id=musica_id).first() if musica_id else None
        except (TypeError, ValueError):
            musica = None
        if not erro and not musica: erro = 'Escolha uma música.'

        if not erro:
            PedidoMusical.objects.create(
                nome_ouvinte=nome,
                localidade=localidade,
                musica=musica,
                tipo_contato=tipo,
                contato=contato,
                mensagem=mensagem,
                aceita_politica=True,
                confirma_dados=True,
                aceita_condicoes=True,
            )
            messages.success(request, 'Pedido enviado com sucesso!')
            return redirect('radio:pedidos')

    return render(request, 'pedidos.html', {'musicas': musicas, 'erro': erro, 'dados': request.POST})
