from django.db import models
from django.utils import timezone

class Jogo(models.Model):
    titulo = models.CharField(max_length=100)
    genero = models.CharField(max_length=50)
    votos = models.PositiveIntegerField(default=0)
    descricao = models.TextField(blank=True, null=True)  # NOVO
    data_cadastro = models.DateTimeField(default=timezone.now)  # NOVO
    plataforma = models.CharField(max_length=100, blank=True, null=True)  # NOVO

    def __str__(self):
        return self.titulo

    class Meta:
        verbose_name = 'Jogo'
        verbose_name_plural = 'Jogos'
        ordering = ['-votos']
    
    # NOVO: Método para calcular porcentagem de votos
    def percentual_votos(self):
        total = Jogo.objects.aggregate(models.Sum('votos'))['votos__sum'] or 0
        if total == 0:
            return 0
        return round((self.votos / total) * 100, 1)