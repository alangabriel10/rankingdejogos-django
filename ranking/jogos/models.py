from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User  # NOVO

class Jogo(models.Model):
    titulo = models.CharField(max_length=100)
    genero = models.CharField(max_length=50)
    votos = models.PositiveIntegerField(default=0)
    descricao = models.TextField(blank=True, null=True)
    data_cadastro = models.DateTimeField(default=timezone.now)
    plataforma = models.CharField(max_length=100, blank=True, null=True)

    def __str__(self):
        return self.titulo

    class Meta:
        verbose_name = 'Jogo'
        verbose_name_plural = 'Jogos'
        ordering = ['-votos']
    
    def percentual_votos(self):
        total = Jogo.objects.aggregate(models.Sum('votos'))['votos__sum'] or 0
        if total == 0:
            return 0
        return round((self.votos / total) * 100, 1)
    
    # NOVO: Verifica se usuário já votou
    def usuario_ja_votou(self, usuario):
        if not usuario.is_authenticated:
            return False
        return Voto.objects.filter(jogo=self, usuario=usuario).exists()


# ===== NOVO MODELO =====
class Voto(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    jogo = models.ForeignKey(Jogo, on_delete=models.CASCADE)
    data_voto = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('usuario', 'jogo')  # Garante 1 voto por usuário por jogo
        verbose_name = 'Voto'
        verbose_name_plural = 'Votos'
        ordering = ['-data_voto']

    def __str__(self):
        return f"{self.usuario.username} votou em {self.jogo.titulo}"