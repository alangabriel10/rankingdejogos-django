from django.views.generic import ListView, CreateView, View, DetailView  # ← Adicione DetailView
from django.urls import reverse_lazy
from django.shortcuts import redirect, get_object_or_404
from .models import Jogo

class ListaJogosView(ListView):
    model = Jogo
    template_name = 'jogos/lista.html'
    context_object_name = 'jogos'
    ordering = ['-votos']

class CriarJogoView(CreateView):
    model = Jogo
    template_name = 'jogos/novo.html'
    fields = ['titulo', 'genero', 'descricao', 'plataforma']  # ← Adicione os novos campos
    success_url = reverse_lazy('lista_jogos')

class VotarJogoView(View):
    def post(self, request, pk):
        jogo = get_object_or_404(Jogo, pk=pk)
        jogo.votos += 1
        jogo.save()
        return redirect('lista_jogos')

# ===== NOVA VIEW =====
class DetalheJogoView(DetailView):
    model = Jogo
    template_name = 'jogos/detalhes.html'
    context_object_name = 'jogo'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Adicionar posição no ranking
        jogos_ordenados = Jogo.objects.order_by('-votos')
        posicao = list(jogos_ordenados).index(self.object) + 1
        context['posicao'] = posicao
        # Adicionar total de jogos
        context['total_jogos'] = Jogo.objects.count()
        return context