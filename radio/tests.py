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

    def test_pedido_pode_ser_listado_editado_e_excluido(self):
        pedido = PedidoMusical.objects.create(
            nome_ouvinte='João', localidade='Capitão Poço', musica=self.musica,
            tipo_contato='telefone', contato='91999991234', aceita_politica=True,
            confirma_dados=True, aceita_condicoes=True,
        )
        resposta = self.client.get(reverse('radio:lista_pedidos'))
        self.assertContains(resposta, 'João')

        resposta = self.client.post(reverse('radio:editar_pedido', args=[pedido.id]), self.pedido(nome_ouvinte='João Silva'))
        self.assertRedirects(resposta, reverse('radio:lista_pedidos'))
        pedido.refresh_from_db()
        self.assertEqual(pedido.nome_ouvinte, 'João Silva')

        resposta = self.client.post(reverse('radio:excluir_pedido', args=[pedido.id]))
        self.assertRedirects(resposta, reverse('radio:lista_pedidos'))
        self.assertFalse(PedidoMusical.objects.filter(id=pedido.id).exists())

    def test_musica_tem_crud_e_nao_exclui_quando_possui_pedido(self):
        resposta = self.client.post(reverse('radio:nova_musica'), {'titulo': 'Melodia 2'})
        self.assertRedirects(resposta, reverse('radio:lista_musicas'))
        musica = Musica.objects.get(titulo='Melodia 2')

        resposta = self.client.post(reverse('radio:editar_musica', args=[musica.id]), {'titulo': 'Melodia 2 atualizada'})
        self.assertRedirects(resposta, reverse('radio:lista_musicas'))
        musica.refresh_from_db()
        self.assertEqual(musica.titulo, 'Melodia 2 atualizada')

        resposta = self.client.post(reverse('radio:excluir_musica', args=[musica.id]))
        self.assertRedirects(resposta, reverse('radio:lista_musicas'))
        self.assertFalse(Musica.objects.filter(id=musica.id).exists())

        PedidoMusical.objects.create(
            nome_ouvinte='Maria', localidade='Belém', musica=self.musica,
            tipo_contato='telefone', contato='91999991234', aceita_politica=True,
            confirma_dados=True, aceita_condicoes=True,
        )
        self.client.post(reverse('radio:excluir_musica', args=[self.musica.id]))
        self.assertTrue(Musica.objects.filter(id=self.musica.id).exists())

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
