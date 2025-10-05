import pygame
import os


class Menu:
    """Menu principal do jogo."""

    def __init__(self, width=800, height=600):
        """
        Inicializa o menu.

        Args:
            width: Largura da tela
            height: Altura da tela
        """
        self.width = width
        self.height = height
        self.background = None
        self.background_path = "assets/images/menu_background.png"

        # Carrega fundo se existir
        if os.path.exists(self.background_path):
            try:
                self.background = pygame.image.load(self.background_path)
                self.background = pygame.transform.scale(self.background, (width, height))
            except Exception as e:
                print(f"Não foi possível carregar fundo: {e}")
                self.background = None

        # Estado do menu
        self.selected_option = 0
        self.options = ["PLAY", "CONFIG", "QUIT"]

        # Cores
        self.bg_color = (20, 20, 30)
        self.title_color = (255, 255, 255)
        self.selected_color = (255, 200, 50)
        self.normal_color = (200, 200, 200)

        # Fontes
        pygame.font.init()
        self.title_font = pygame.font.Font(None, 80)
        self.option_font = pygame.font.Font(None, 60)

    def handle_event(self, event):
        """
        Trata eventos de entrada do menu.

        Args:
            event: evento pygame

        Returns:
            str: Ação a tomar ('play', 'quit', None)
        """
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                self.selected_option = (self.selected_option - 1) % len(self.options)
            elif event.key == pygame.K_DOWN:
                self.selected_option = (self.selected_option + 1) % len(self.options)
            elif event.key == pygame.K_RETURN or event.key == pygame.K_SPACE:
                if self.selected_option == 0:  # PLAY
                    return 'play'
                elif self.selected_option == 1:  # CONFIG
                    return 'config'
                elif self.selected_option == 2:  # QUIT
                    return 'quit'
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            # Verifica se está clicando nos botões
            for i in range(len(self.options)):
                if self._get_option_rect(i).collidepoint(mouse_pos):
                    if i == 0:
                        return 'play'
                    elif i == 1:
                        return 'config'
                    elif i == 2:
                        return 'quit'
        elif event.type == pygame.MOUSEMOTION:
            mouse_pos = pygame.mouse.get_pos()
            # Destaca opção ao passar o mouse
            for i in range(len(self.options)):
                if self._get_option_rect(i).collidepoint(mouse_pos):
                    self.selected_option = i
                    break

        return None

    def _get_option_rect(self, option_index):
        """Obtém o retângulo para uma opção do menu."""
        y_start = self.height // 2 + 50
        y_spacing = 80
        y = y_start + option_index * y_spacing

        text = self.option_font.render(self.options[option_index], True, self.normal_color)
        x = self.width // 2 - text.get_width() // 2

        return pygame.Rect(x, y, text.get_width(), text.get_height())

    def render(self, screen):
        """
        Renderiza o menu.

        Args:
            screen: superfície pygame para renderizar
        """
        # Desenha fundo
        if self.background:
            screen.blit(self.background, (0, 0))
        else:
            screen.fill(self.bg_color)

        # Desenha título
        title_text = self.title_font.render("DREAMROOMS", True, self.title_color)
        title_x = self.width // 2 - title_text.get_width() // 2
        title_y = self.height // 3
        screen.blit(title_text, (title_x, title_y))

        # Desenha opções
        y_start = self.height // 2 + 50
        y_spacing = 80

        for i, option in enumerate(self.options):
            color = self.selected_color if i == self.selected_option else self.normal_color
            text = self.option_font.render(option, True, color)
            x = self.width // 2 - text.get_width() // 2
            y = y_start + i * y_spacing
            screen.blit(text, (x, y))

            # Desenha indicador de seleção
            if i == self.selected_option:
                indicator = self.option_font.render(">", True, self.selected_color)
                screen.blit(indicator, (x - 50, y))
