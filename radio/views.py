from django.contrib import messages
from django.db.models import ProtectedError
from django.shortcuts import get_object_or_404, redirect, render

from .forms import MusicaForm, PedidoMusicalForm
from .models import Musica, PedidoMusical


def index(request): return render(request, 'index.html')


def pedidos(request):
    form = PedidoMusicalForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, 'Pedido enviado com sucesso!')
        return redirect('radio:pedidos')
    return render(request, 'pedidos.html', {'form': form})


def lista_pedidos(request):
    termo = request.GET.get('busca', '').strip()
    lista = PedidoMusical.objects.select_related('musica')
    if termo:
        lista = lista.filter(nome_ouvinte__icontains=termo)
    return render(request, 'lista_pedidos.html', {'pedidos': lista, 'busca': termo})


def editar_pedido(request, pedido_id):
    pedido = get_object_or_404(PedidoMusical, id=pedido_id)
    form = PedidoMusicalForm(request.POST or None, instance=pedido)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, 'Pedido atualizado com sucesso!')
        return redirect('radio:lista_pedidos')
    return render(request, 'pedidos.html', {'form': form, 'pedido': pedido})


def excluir_pedido(request, pedido_id):
    pedido = get_object_or_404(PedidoMusical, id=pedido_id)
    if request.method == 'POST':
        pedido.delete()
        messages.success(request, 'Pedido excluído com sucesso!')
    return redirect('radio:lista_pedidos')


def lista_musicas(request):
    return render(request, 'lista_musicas.html', {'musicas': Musica.objects.all()})


def nova_musica(request):
    form = MusicaForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, 'Música cadastrada com sucesso!')
        return redirect('radio:lista_musicas')
    return render(request, 'form_musica.html', {'form': form})


def editar_musica(request, musica_id):
    musica = get_object_or_404(Musica, id=musica_id)
    form = MusicaForm(request.POST or None, instance=musica)
    if request.method == 'POST' and form.is_valid():
        form.save()
        messages.success(request, 'Música atualizada com sucesso!')
        return redirect('radio:lista_musicas')
    return render(request, 'form_musica.html', {'form': form, 'musica': musica})


def excluir_musica(request, musica_id):
    musica = get_object_or_404(Musica, id=musica_id)
    if request.method == 'POST':
        try:
            musica.delete()
            messages.success(request, 'Música excluída com sucesso!')
        except ProtectedError:
            messages.error(request, 'Essa música possui pedidos e não pode ser excluída.')
    return redirect('radio:lista_musicas')
