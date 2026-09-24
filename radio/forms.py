import re

from django import forms
from django.core.exceptions import ValidationError
from django.core.validators import validate_email

from .models import Musica, PedidoMusical


class PedidoMusicalForm(forms.ModelForm):
    class Meta:
        model = PedidoMusical
        fields = [
            'nome_ouvinte', 'localidade', 'musica', 'tipo_contato', 'contato',
            'mensagem', 'aceita_politica', 'confirma_dados', 'aceita_condicoes',
        ]
        widgets = {
            'nome_ouvinte': forms.TextInput(attrs={'class': 'form-control'}),
            'localidade': forms.TextInput(attrs={'class': 'form-control'}),
            'musica': forms.Select(attrs={'class': 'form-select'}),
            'tipo_contato': forms.RadioSelect(),
            'contato': forms.TextInput(attrs={'class': 'form-control'}),
            'mensagem': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'aceita_politica': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'confirma_dados': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'aceita_condicoes': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }

    def clean_contato(self):
        contato = self.cleaned_data.get('contato', '').strip()
        tipo = self.cleaned_data.get('tipo_contato')

        if tipo == 'email':
            try:
                validate_email(contato)
            except ValidationError:
                raise forms.ValidationError('Digite um e-mail válido.')
        elif tipo == 'telefone':
            numeros = ''.join(numero for numero in contato if numero.isdigit())
            if not re.fullmatch(r'[\d\s()+-]{8,20}', contato) or len(numeros) < 8:
                raise forms.ValidationError('Digite um telefone válido.')

        return contato

    def clean(self):
        dados = super().clean()
        confirmacoes = ['aceita_politica', 'confirma_dados', 'aceita_condicoes']
        if not all(dados.get(campo) for campo in confirmacoes):
            raise forms.ValidationError('Marque as três confirmações.')
        return dados


class MusicaForm(forms.ModelForm):
    class Meta:
        model = Musica
        fields = ['titulo']
        widgets = {'titulo': forms.TextInput(attrs={'class': 'form-control'})}
