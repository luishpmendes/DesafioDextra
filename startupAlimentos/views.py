from django.shortcuts import get_object_or_404, render
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
from django.views import generic

from .models import Ingrediente, Lanche, LancheIngrediente
from .forms import LancheForm

class IndexView(generic.ListView):
    template_name = 'startupAlimentos/index.html'
    context_object_name = 'lanches'

    def get_queryset(self):
        return Lanche.objects.all()

class DetailView(generic.DetailView):
    model = Lanche
    template_name = 'startupAlimentos/detail.html'

def pedir(request, lanche_id):
    lanche = get_object_or_404(Lanche, pk=lanche_id)
    return HttpResponseRedirect(reverse('startupAlimentos:index'))

def montarLanche(request):
    ingredientes = Ingrediente.objects.all()
    if request.method == 'GET':
        form = LancheForm(ingredientes=ingredientes)
    else:
        form = LancheForm(request.POST, ingredientes=ingredientes)
        print ("form")
        if form.is_valid():
            nome = form.cleaned_data['nome']
            lanche = Lanche(nome=nome)
            lanche.save()
            for ingrediente in ingredientes:
                quantidade = form.cleaned_data['ingrediente-' + str(ingrediente.id)]
                lanche_ingrediente = LancheIngrediente(lanche=lanche, ingrediente=ingrediente, quantidade=quantidade)
                lanche_ingrediente.save()
            return HttpResponseRedirect(reverse('startupAlimentos:index'))
    return render(request, 'startupAlimentos/montarLanche.html', {'form': form, 'ingredientes': ingredientes,})
