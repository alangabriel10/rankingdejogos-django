from django.views.generic import ListView, CreateView, DetailView, View
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.shortcuts import redirect, get_object_or_404
from django.contrib import messages
from django.db import IntegrityError
from .models import Jogo, Voto


# ===== VIEWS DE JOGOS =====

class ListaJogosView(ListView):
    model = Jogo
    template_name = 'jogos/lista.html'
    context_object_name = 'jogos'
    ordering = ['-votos']
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Adiciona info de quais jogos o usuário já votou
        if self.request.user.is_authenticated:
            votos_usuario = Voto.objects.filter(
                usuario=self.request.user
            ).values_list('jogo_id', flat=True)
            context['votos_usuario'] = list(votos_usuario)
        else:
            context['votos_usuario'] = []
        return context


class CriarJogoView(LoginRequiredMixin, CreateView):
    model = Jogo
    template_name = 'jogos/novo.html'
    fields = ['titulo', 'genero', 'descricao', 'plataforma']
    success_url = reverse_lazy('lista_jogos')
    login_url = 'login'  # Redireciona para login se não autenticado


class DetalheJogoView(DetailView):
    model = Jogo
    template_name = 'jogos/detalhes.html'
    context_object_name = 'jogo'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Posição no ranking
        jogos_ordenados = Jogo.objects.order_by('-votos')
        posicao = list(jogos_ordenados).index(self.object) + 1
        context['posicao'] = posicao
        context['total_jogos'] = Jogo.objects.count()
        
        # Verifica se usuário já votou
        if self.request.user.is_authenticated:
            context['ja_votou'] = self.object.usuario_ja_votou(self.request.user)
        else:
            context['ja_votou'] = False
            
        return context


class VotarJogoView(LoginRequiredMixin, View):
    login_url = 'login'
    
    def post(self, request, pk):
        jogo = get_object_or_404(Jogo, pk=pk)
        
        # Tenta criar o voto
        try:
            Voto.objects.create(usuario=request.user, jogo=jogo)
            jogo.votos += 1
            jogo.save()
            messages.success(request, f'Voto em "{jogo.titulo}" registrado com sucesso! 🎉')
        except IntegrityError:
            # Usuário já votou neste jogo
            messages.warning(request, f'Você já votou em "{jogo.titulo}"!')
        
        return redirect('lista_jogos')


# ===== VIEWS DE AUTENTICAÇÃO =====

class RegistroView(CreateView):
    form_class = UserCreationForm
    template_name = 'jogos/registro.html'
    success_url = reverse_lazy('login')
    
    def form_valid(self, form):
        response = super().form_valid(form)
        messages.success(self.request, 'Conta criada com sucesso! 🎉 Faça login para continuar.')
        return response
    
    def get(self, request, *args, **kwargs):
        # Se usuário já estiver logado, redireciona para home
        if request.user.is_authenticated:
            return redirect('lista_jogos')
        return super().get(request, *args, **kwargs)


class MeuLoginView(LoginView):
    template_name = 'jogos/login.html'
    
    def get_success_url(self):
        messages.success(self.request, f'Bem-vindo(a), {self.request.user.username}! 🎮')
        return reverse_lazy('lista_jogos')
    
    def get(self, request, *args, **kwargs):
        # Se usuário já estiver logado, redireciona para home
        if request.user.is_authenticated:
            return redirect('lista_jogos')
        return super().get(request, *args, **kwargs)


class MeuLogoutView(LogoutView):
    next_page = 'lista_jogos'
    
    def dispatch(self, request, *args, **kwargs):
        messages.info(request, 'Você saiu da sua conta. Até logo! 👋')
        return super().dispatch(request, *args, **kwargs)


# ===== VIEW DE PERFIL =====

class PerfilView(LoginRequiredMixin, ListView):
    model = Voto
    template_name = 'jogos/perfil.html'
    context_object_name = 'votos'
    login_url = 'login'
    
    def get_queryset(self):
        return Voto.objects.filter(usuario=self.request.user).select_related('jogo')