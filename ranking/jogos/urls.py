from django.urls import path
from . import views

urlpatterns = [
    path('', views.ListaJogosView.as_view(), name='lista_jogos'),
    path('novo/', views.CriarJogoView.as_view(), name='criar_jogo'),
    path('<int:pk>/votar/', views.VotarJogoView.as_view(), name='votar_jogo'),
    path('<int:pk>/', views.DetalheJogoView.as_view(), name='detalhes_jogo'),  # NOVA ROTA
]