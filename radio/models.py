from django.db import models


class Musica(models.Model):
    titulo = models.CharField('título', max_length=150)

    class Meta:
        verbose_name = 'música'; verbose_name_plural = 'músicas'
        ordering = ['titulo']

    def __str__(self): return self.titulo


class PedidoMusical(models.Model):
    CONTATOS = [('telefone', 'Telefone'), ('email', 'E-mail')]

    nome_ouvinte = models.CharField('nome', max_length=100); localidade = models.CharField('localidade', max_length=120)
    musica = models.ForeignKey(Musica, verbose_name='música', on_delete=models.PROTECT)
    tipo_contato = models.CharField('tipo de contato', max_length=10, choices=CONTATOS)
    contato = models.CharField('telefone ou e-mail', max_length=150)
    mensagem = models.TextField(blank=True)
    aceita_politica = models.BooleanField('aceitou a política de privacidade')
    confirma_dados = models.BooleanField('confirmou os dados')
    aceita_condicoes = models.BooleanField('aceitou as condições')
    data = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'pedido musical'
        verbose_name_plural = 'pedidos musicais'
        ordering = ['-data']

    def __str__(self): return f'{self.nome_ouvinte} - {self.musica}'
