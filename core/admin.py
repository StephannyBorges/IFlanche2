from django.contrib import admin
from .models import Cardapio, Aluno

@admin.register(Cardapio)
class CardapioAdmin(admin.ModelAdmin):
    # AQUI ESTAVA O ERRO: Mudamos de 'cafe_manha' para 'lanche_manha'
    list_display = ('dia_semana', 'lanche_manha', 'almoco', 'lanche_tarde')
    list_editable = ('lanche_manha', 'almoco', 'lanche_tarde')

@admin.register(Aluno)
class AlunoAdmin(admin.ModelAdmin):
    list_display = ('nome', 'matricula', 'curso')