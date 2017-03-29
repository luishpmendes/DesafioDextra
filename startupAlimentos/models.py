from django.db import models
from django.utils.encoding import python_2_unicode_compatible


@python_2_unicode_compatible
class Promocao(models.Model):
    nome = models.CharField(max_length=100)
    regra_de_negocio = models.CharField(max_length=300)
    esta_ativa = models.BooleanField(default=False)
    def __str__(self):
        return self.nome

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
        result = 0
        muitaCarneAtiva = False
        if (len(Promocao.objects.filter(nome="Muita carne")) > 0): # se existe a promoção Muita carne
            muitaCarne = Promocao.objects.filter(nome="Muita carne")[0]
            muitaCarneAtiva = muitaCarne.esta_ativa
        muitoQueijoAtiva = False
        if (len(Promocao.objects.filter(nome="Muita queijo")) > 0): # se existe a promoção Muita queijo
            muitoQueijo = Promocao.objects.filter(nome="Muita queijo")[0]
            muitoQueijoAtiva = muitaCarne.esta_ativa
        for ingrediente in self.ingredientes.all():
            lanche_ingrediente = LancheIngrediente.objects.get(lanche=self, ingrediente=ingrediente)
            result += lanche_ingrediente.quantidade * ingrediente.valor
            if (ingrediente.nome == "Hambúrguer de carne" and muitaCarneAtiva):
                result -= (lanche_ingrediente.quantidade // 3) * ingrediente.valor
            if (ingrediente.nome == "Queijo" and muitoQueijoAtiva):
                result -= (lanche_ingrediente.quantidade // 3) * ingrediente.valor
        if (len(Promocao.objects.filter(nome="Light")) > 0): # se existe a promoção Light
            light = Promocao.objects.filter(nome="Light")[0]
            if (light.esta_ativa): # se a promoção Light está ativa
                if (len(self.ingredientes.filter(nome="alface")) > 0 and self.ingredientes.filter(nome="alface")[0].quantidade > 0): # se o lanche possui alface
                    if (len(self.ingredientes.filter(nome="bacon")) <= 0 or self.ingredientes.filter(nome="bacon")[0].quantidade <= 0): # se o lanche não possui bacon
                        result = 0.9 * result
        return result

class LancheIngrediente(models.Model):
    lanche = models.ForeignKey(Lanche, on_delete=models.CASCADE)
    ingrediente = models.ForeignKey(Ingrediente, on_delete=models.CASCADE)
    quantidade = models.IntegerField(default=1)
