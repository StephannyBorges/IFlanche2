from django.db import models
from django.contrib.auth.models import User

# --- MODELO ALUNO (Recuperado) ---
class Aluno(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    nome = models.CharField(max_length=100)
    matricula = models.CharField(max_length=20, unique=True)
    curso = models.CharField(max_length=100)
    foto = models.ImageField(upload_to='perfil_fotos/', blank=True, null=True)

    def __str__(self):
        return self.nome

# --- MODELO CARDAPIO (Novo e Corrigido) ---
class Cardapio(models.Model):
    DIAS = [
        ('Segunda-feira', 'Segunda-feira'),
        ('Terça-feira', 'Terça-feira'),
        ('Quarta-feira', 'Quarta-feira'),
        ('Quinta-feira', 'Quinta-feira'),
        ('Sexta-feira', 'Sexta-feira'),
    ]

    dia_semana = models.CharField(max_length=20, choices=DIAS, unique=True)
    lanche_manha = models.CharField(max_length=200, blank=True, null=True, verbose_name="Lanche da Manhã")
    almoco = models.CharField(max_length=200, blank=True, null=True, verbose_name="Almoço")
    lanche_tarde = models.CharField(max_length=200, blank=True, null=True, verbose_name="Lanche da Tarde")

    def __str__(self):
        return self.dia_semana

    class Meta:
        verbose_name = "Cardápio"
        verbose_name_plural = "Cardápios"
        ordering = ['id']