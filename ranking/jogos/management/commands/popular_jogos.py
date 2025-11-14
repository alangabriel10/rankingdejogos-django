from django.core.management.base import BaseCommand
from jogos.models import Jogo

class Command(BaseCommand):
    help = 'Popula o banco de dados com jogos iniciais'

    def handle(self, *args, **kwargs):
        jogos_iniciais = [
            {
                'titulo': 'Fortnite',
                'genero': 'Battle Royale',
                'descricao': 'Jogo de battle royale gratuito onde 100 jogadores competem para ser o último sobrevivente. Inclui construção, combate intenso e eventos ao vivo.',
                'plataforma': 'PC, PS5, Xbox, Nintendo Switch, Mobile'
            },
            {
                'titulo': 'Call of Duty: Warzone',
                'genero': 'Battle Royale/FPS',
                'descricao': 'Battle royale intenso ambientado no universo de Call of Duty. Combate tático com até 150 jogadores em mapas massivos.',
                'plataforma': 'PC, PS5, Xbox'
            },
            {
                'titulo': 'Apex Legends',
                'genero': 'Battle Royale/FPS',
                'descricao': 'Battle royale baseado em heróis com habilidades únicas. Combate rápido e fluido em esquadrões de 3 jogadores.',
                'plataforma': 'PC, PS5, Xbox, Nintendo Switch'
            },
            {
                'titulo': 'Overwatch',
                'genero': 'FPS/Hero Shooter',
                'descricao': 'Shooter em equipe baseado em objetivos com heróis únicos. Cada personagem tem habilidades especiais e estilos de jogo distintos.',
                'plataforma': 'PC, PS5, Xbox, Nintendo Switch'
            },
            {
                'titulo': 'Rocket League',
                'genero': 'Esportes/Arcade',
                'descricao': 'Futebol com carros! Partidas competitivas onde jogadores usam carros acrobáticos para marcar gols com uma bola gigante.',
                'plataforma': 'PC, PS5, Xbox, Nintendo Switch'
            },
        ]

        jogos_criados = 0
        jogos_existentes = 0

        for jogo_data in jogos_iniciais:
            jogo, criado = Jogo.objects.get_or_create(
                titulo=jogo_data['titulo'],
                defaults={
                    'genero': jogo_data['genero'],
                    'descricao': jogo_data['descricao'],
                    'plataforma': jogo_data['plataforma'],
                    'votos': 0
                }
            )

            if criado:
                jogos_criados += 1
                self.stdout.write(
                    self.style.SUCCESS(f'✅ Jogo "{jogo.titulo}" criado com sucesso!')
                )
            else:
                jogos_existentes += 1
                self.stdout.write(
                    self.style.WARNING(f'⚠️  Jogo "{jogo.titulo}" já existe no banco.')
                )

        self.stdout.write(
            self.style.SUCCESS(f'\n🎉 Processo concluído!')
        )
        self.stdout.write(f'📊 Jogos criados: {jogos_criados}')
        self.stdout.write(f'📊 Jogos já existentes: {jogos_existentes}')