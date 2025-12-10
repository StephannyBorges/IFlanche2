from django.db import models

# Create your models here.
from django.db import models

class Cardapio(models.Model):
    dia_semana = models.CharField(max_length=50) 
    cafe_manha = models.CharField(max_length=200)
    almoco = models.CharField(max_length=200)
    lanche_tarde = models.CharField(max_length=200)

    def __str__(self):
        return self.dia_semana