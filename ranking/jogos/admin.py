from django.contrib import admin
from .models import Jogo, Voto

@admin.register(Jogo)
class JogoAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'genero', 'votos', 'plataforma', 'data_cadastro')
    list_filter = ('genero', 'plataforma')
    search_fields = ('titulo', 'descricao')
    date_hierarchy = 'data_cadastro'


@admin.register(Voto)
class VotoAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'jogo', 'data_voto')
    list_filter = ('data_voto',)
    search_fields = ('usuario__username', 'jogo__titulo')
    date_hierarchy = 'data_voto'