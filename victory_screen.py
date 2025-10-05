import pygame
import os


class VictoryScreen:
    """Tela de vitória com créditos que aparece quando o jogador vence."""

    OUTRO_MUSIC_PATH = "assets/audio/outro.mp3"

    def __init__(self, width=800, height=600):
        """
        Inicializa a tela de vitória.

        Args:
            width: Largura da tela
            height: Altura da tela
        """
        self.width = width
        self.height = height

        # Cores
        self.bg_color = (10, 10, 20)
        self.title_color = (255, 215, 0)  # Dourado
        self.credit_color = (200, 200, 200)

        # Fontes
        pygame.font.init()
        self.title_font = pygame.font.Font(None, 100)
        self.credit_font = pygame.font.Font(None, 50)
        self.name_font = pygame.font.Font(None, 40)

        # Créditos
        self.credits = [
            ("Game Director", "Sarah Mitchell"),
            ("Lead Programmer", "Alex Chen"),
            ("Level Designer", "Marcus Rodriguez"),
            ("Sound Designer", "Emily Thompson"),
        ]

        # Estado de rolagem
        self.scroll_y = height
        self.scroll_speed = 30.0  # pixels por segundo

        # Carrega música de encerramento
        self._load_outro_music()

    def _load_outro_music(self):
        """Carrega e reproduz música de encerramento."""
        if os.path.exists(self.OUTRO_MUSIC_PATH):
            try:
                pygame.mixer.music.load(self.OUTRO_MUSIC_PATH)
                pygame.mixer.music.play(-1)  # Loop
            except Exception as e:
                print(f"Não foi possível carregar música de encerramento: {e}")

    def update(self, delta_time):
        """
        Atualiza rolagem dos créditos.

        Args:
            delta_time: Tempo desde a última atualização
        """
        self.scroll_y -= self.scroll_speed * delta_time

    def handle_event(self, event):
        """
        Trata eventos de entrada da tela de vitória.

        Args:
            event: evento pygame

        Returns:
            str: Ação a tomar ('quit', 'menu', None)
        """
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE or event.key == pygame.K_RETURN:
                return 'menu'
        elif event.type == pygame.MOUSEBUTTONDOWN:
            return 'menu'

        return None

    def render(self, screen):
        """
        Renderiza a tela de vitória.

        Args:
            screen: superfície pygame para renderizar
        """
        # Fundo
        screen.fill(self.bg_color)

        # Título de vitória
        title_text = self.title_font.render("VICTORY!", True, self.title_color)
        title_x = self.width // 2 - title_text.get_width() // 2
        screen.blit(title_text, (title_x, 100))

        # Créditos (rolagem)
        current_y = self.scroll_y

        for role, name in self.credits:
            # Função
            role_text = self.credit_font.render(role, True, self.credit_color)
            role_x = self.width // 2 - role_text.get_width() // 2
            if -50 < current_y < self.height + 50:  # Só renderiza se visível
                screen.blit(role_text, (role_x, current_y))
            current_y += 60

            # Nome
            name_text = self.name_font.render(name, True, self.title_color)
            name_x = self.width // 2 - name_text.get_width() // 2
            if -50 < current_y < self.height + 50:  # Só renderiza se visível
                screen.blit(name_text, (name_x, current_y))
            current_y += 80

        # Instruções na parte inferior
        inst_font = pygame.font.Font(None, 30)
        inst_text = inst_font.render("Press ESC or click to return to menu", True, self.credit_color)
        screen.blit(inst_text, (self.width // 2 - inst_text.get_width() // 2, self.height - 50))
