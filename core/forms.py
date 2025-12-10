from django import forms
from .models import Cardapio
from .models import Aluno 

class CardapioForm(forms.ModelForm):
    class Meta:
        model = Cardapio
        fields = ['dia_semana', 'cafe_manha', 'almoco', 'lanche_tarde']
        # Aqui estilizamos os inputs para ficarem bonitos no HTML (opcional)
        widgets = {
            'dia_semana': forms.Select(choices=[
                ('Segunda-feira', 'Segunda-feira'),
                ('Terça-feira', 'Terça-feira'),
                ('Quarta-feira', 'Quarta-feira'),
                ('Quinta-feira', 'Quinta-feira'),
                ('Sexta-feira', 'Sexta-feira')
            ], attrs={'class': 'input-select'}),
            'cafe_manha': forms.TextInput(attrs={'class': 'input-text', 'placeholder': 'Ex: Fruta + Iogurte'}),
            'almoco': forms.TextInput(attrs={'class': 'input-text', 'placeholder': 'Ex: Feijoada'}),
            'lanche_tarde': forms.TextInput(attrs={'class': 'input-text', 'placeholder': 'Ex: Bolo'}),
        }

class AlunoPerfilForm(forms.ModelForm):
    class Meta:
        model = Aluno
        # Aqui dizemos que só queremos mostrar o campo da foto no formulário
        fields = ['foto_perfil']