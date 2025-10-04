import pygame
import os


class Menu:
    """Main menu for the game."""

    def __init__(self, width=800, height=600):
        """
        Initialize the menu.

        Args:
            width: Screen width
            height: Screen height
        """
        self.width = width
        self.height = height
        self.background = None
        self.background_path = "assets/images/menu_background.png"

        # Load background if it exists
        if os.path.exists(self.background_path):
            try:
                self.background = pygame.image.load(self.background_path)
                self.background = pygame.transform.scale(self.background, (width, height))
            except Exception as e:
                print(f"Could not load background: {e}")
                self.background = None

        # Menu state
        self.selected_option = 0
        self.options = ["PLAY", "CONFIG", "QUIT"]

        # Colors
        self.bg_color = (20, 20, 30)
        self.title_color = (255, 255, 255)
        self.selected_color = (255, 200, 50)
        self.normal_color = (200, 200, 200)

        # Fonts
        pygame.font.init()
        self.title_font = pygame.font.Font(None, 80)
        self.option_font = pygame.font.Font(None, 60)

    def handle_event(self, event):
        """
        Handle menu input events.

        Args:
            event: pygame event

        Returns:
            str: Action to take ('play', 'quit', None)
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
            # Check if clicking on buttons
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
            # Highlight option on hover
            for i in range(len(self.options)):
                if self._get_option_rect(i).collidepoint(mouse_pos):
                    self.selected_option = i
                    break

        return None

    def _get_option_rect(self, option_index):
        """Get the rectangle for a menu option."""
        y_start = self.height // 2 + 50
        y_spacing = 80
        y = y_start + option_index * y_spacing

        text = self.option_font.render(self.options[option_index], True, self.normal_color)
        x = self.width // 2 - text.get_width() // 2

        return pygame.Rect(x, y, text.get_width(), text.get_height())

    def render(self, screen):
        """
        Render the menu.

        Args:
            screen: pygame surface to render to
        """
        # Draw background
        if self.background:
            screen.blit(self.background, (0, 0))
        else:
            screen.fill(self.bg_color)

        # Draw title
        title_text = self.title_font.render("CRAZY BACKROOMS", True, self.title_color)
        title_x = self.width // 2 - title_text.get_width() // 2
        title_y = self.height // 3
        screen.blit(title_text, (title_x, title_y))

        # Draw options
        y_start = self.height // 2 + 50
        y_spacing = 80

        for i, option in enumerate(self.options):
            color = self.selected_color if i == self.selected_option else self.normal_color
            text = self.option_font.render(option, True, color)
            x = self.width // 2 - text.get_width() // 2
            y = y_start + i * y_spacing
            screen.blit(text, (x, y))

            # Draw selection indicator
            if i == self.selected_option:
                indicator = self.option_font.render(">", True, self.selected_color)
                screen.blit(indicator, (x - 50, y))
