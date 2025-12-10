from django.contrib import admin
from .models import Cardapio

# Configura como a tabela aparece no painel /admin/
@admin.register(Cardapio)
class CardapioAdmin(admin.ModelAdmin):
    list_display = ('dia_semana', 'cafe_manha', 'almoco', 'lanche_tarde')
    list_filter = ('dia_semana',)
    search_fields = ('dia_semana', 'almoco')
    