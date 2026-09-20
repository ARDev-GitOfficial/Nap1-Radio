from django.urls import path
from . import views

app_name = 'radio'

urlpatterns = [
    path('', views.index, name='index'),
    path('pedir-musica/', views.pedidos, name='pedidos')]
