from django.urls import path
from . import views

urlpatterns = [
    # Jogos
    path('', views.ListaJogosView.as_view(), name='lista_jogos'),
    path('<int:pk>/', views.DetalheJogoView.as_view(), name='detalhes_jogo'),
    path('<int:pk>/votar/', views.VotarJogoView.as_view(), name='votar_jogo'),
    
    # Autenticação
    path('registro/', views.RegistroView.as_view(), name='registro'),
    path('login/', views.MeuLoginView.as_view(), name='login'),
    path('logout/', views.MeuLogoutView.as_view(), name='logout'),
    path('perfil/', views.PerfilView.as_view(), name='perfil'),
]