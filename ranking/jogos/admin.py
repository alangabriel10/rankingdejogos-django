from django.contrib import admin
from .models import Jogo

@admin.register(Jogo)
class JogoAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'genero', 'votos', 'plataforma', 'data_cadastro')
    list_filter = ('genero', 'plataforma')
    search_fields = ('titulo', 'descricao')
    date_hierarchy = 'data_cadastro'