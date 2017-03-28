from django.db import models
from django.utils.encoding import python_2_unicode_compatible


@python_2_unicode_compatible
class Ingrediente(models.Model):
    nome = models.CharField(max_length=100)
    valor = models.DecimalField(max_digits=5, decimal_places=2, default=0.00)
    def __str__(self):
        return self.nome

@python_2_unicode_compatible
class Lanche(models.Model):
    nome = models.CharField(max_length=100)
    ingredientes = models.ManyToManyField(Ingrediente)
    def __str__(self):
        return self.nome

@python_2_unicode_compatible
class Promocao(models.Model):
    nome = models.CharField(max_length=100)
    regra_de_negocio = models.CharField(max_length=300)
    esta_ativa = models.BooleanField(default=False)
    def __str__(self):
        return self.nome
