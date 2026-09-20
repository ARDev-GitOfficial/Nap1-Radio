from django.test import TestCase
from django.urls import reverse

from .models import Musica, PedidoMusical


class RadioTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.musica = Musica.objects.create(titulo='Melodia 1')

    def pedido(self, **mudancas):
        dados = {
            'nome_ouvinte': 'Maria',
            'localidade': 'Belém',
            'musica': self.musica.id,
            'tipo_contato': 'telefone',
            'contato': '(91) 99999-1234',
            'mensagem': 'Quero ouvir essa música.',
            'aceita_politica': 'on',
            'confirma_dados': 'on',
            'aceita_condicoes': 'on',
        }
        dados.update(mudancas)
        return dados

    def test_paginas_abrem(self):
        self.assertEqual(self.client.get(reverse('radio:index')).status_code, 200); self.assertEqual(self.client.get(reverse('radio:pedidos')).status_code, 200)

    def test_pedido_e_salvo(self):
        resposta = self.client.post(reverse('radio:pedidos'), self.pedido())
        self.assertRedirects(resposta, reverse('radio:pedidos'))
        self.assertEqual(PedidoMusical.objects.count(), 1)

    def test_email_invalido_nao_e_salvo(self):
        resposta = self.client.post(reverse('radio:pedidos'), self.pedido(
            tipo_contato='email', contato='email-invalido'
        ))
        self.assertEqual(resposta.status_code, 200)
        self.assertFalse(PedidoMusical.objects.exists())

    def test_confirmacoes_sao_obrigatorias(self):
        dados = self.pedido()
        dados.pop('aceita_politica')
        resposta = self.client.post(reverse('radio:pedidos'), dados)
        self.assertEqual(resposta.status_code, 200)
        self.assertFalse(PedidoMusical.objects.exists())

    def test_admin_exige_login(self):
        self.assertRedirects(self.client.get('/admin/'), '/admin/login/?next=/admin/')
