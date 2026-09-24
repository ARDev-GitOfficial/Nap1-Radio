from django.urls import path
from . import views

app_name = 'radio'

urlpatterns = [
    path('', views.index, name='index'),
    path('pedir-musica/', views.pedidos, name='pedidos'),
    path('pedidos/', views.lista_pedidos, name='lista_pedidos'),
    path('pedidos/<int:pedido_id>/editar/', views.editar_pedido, name='editar_pedido'),
    path('pedidos/<int:pedido_id>/excluir/', views.excluir_pedido, name='excluir_pedido'),
    path('musicas/', views.lista_musicas, name='lista_musicas'),
    path('musicas/nova/', views.nova_musica, name='nova_musica'),
    path('musicas/<int:musica_id>/editar/', views.editar_musica, name='editar_musica'),
    path('musicas/<int:musica_id>/excluir/', views.excluir_musica, name='excluir_musica'),
]
