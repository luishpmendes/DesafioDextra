import decimal

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
    ingredientes = models.ManyToManyField(Ingrediente, through='LancheIngrediente')
    def __str__(self):
        return self.nome
    def valor(self):
        result = decimal.Decimal('0.0')
        for ingrediente in self.ingredientes.all():
            lanche_ingrediente = LancheIngrediente.objects.get(lanche=self, ingrediente=ingrediente)
            result += lanche_ingrediente.quantidade * ingrediente.valor
            if (ingrediente.nome == "Hambúrguer de carne"):
                result -= (lanche_ingrediente.quantidade // 3) * ingrediente.valor # aplica promoção Muita Carne
            if (ingrediente.nome == "Queijo"):
                result -= (lanche_ingrediente.quantidade // 3) * ingrediente.valor # aplica promoção Muito Queijo
        if (len(self.ingredientes.filter(nome="Alface")) > 0 and LancheIngrediente.objects.get(lanche=self, ingrediente=self.ingredientes.filter(nome="Alface")[0]).quantidade > 0): # se o lanche possui Alface
            if (len(self.ingredientes.filter(nome="Bacon")) <= 0 or LancheIngrediente.objects.get(lanche=self, ingrediente=self.ingredientes.filter(nome="Bacon")[0]).quantidade <= 0): # se o lanche não possui Bacon
                result *= decimal.Decimal('0.9') # aplica promoção Light
        return result.quantize(decimal.Decimal('.01'))

class LancheIngrediente(models.Model):
    lanche = models.ForeignKey(Lanche, on_delete=models.CASCADE)
    ingrediente = models.ForeignKey(Ingrediente, on_delete=models.CASCADE)
    quantidade = models.IntegerField(default=1)
