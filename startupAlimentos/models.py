from django.db import models


class Ingrediente(models.Model):
    nome = models.CharField(max_length=100)
    valor = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)

class Lanche(models.Model):
    nome = models.CharField(max_length=100)
    ingredientes = models.ManyToManyField(Ingrediente)

class Promocao(models.Model):
    nome = models.CharField(max_length=100)
    regra_de_negocio = models.CharField(max_length=300)
    esta_ativa = models.BooleanField(default=False)
