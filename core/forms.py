from django import forms
from .models import Cardapio, Aluno

class CardapioForm(forms.ModelForm):
    class Meta:
        model = Cardapio
        # CORREÇÃO: Aqui estava 'cafe_manha', mudamos para 'lanche_manha'
        fields = ['dia_semana', 'lanche_manha', 'almoco', 'lanche_tarde']

class AlunoForm(forms.ModelForm):
    class Meta:
        model = Aluno
        fields = ['foto'] # Usado para o aluno enviar a foto de perfil