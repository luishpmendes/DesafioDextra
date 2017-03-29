from django import forms

from .models import Ingrediente, Lanche, LancheIngrediente

class LancheForm(forms.Form):
    nome = forms.CharField(label='Nome', max_length=100)

    def __init__(self, *args, **kwargs):
        ingredientes = kwargs.pop('ingredientes')
        super(LancheForm, self).__init__(*args, **kwargs)
        for ingrediente in ingredientes:
            self.fields['ingrediente-'+str(ingrediente.id)] = forms.IntegerField(label=ingrediente.nome, initial=0, min_value=0)
