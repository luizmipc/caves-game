import pygame
import os


class VictoryScreen:
    """Victory screen with credits that shows when player wins."""

    OUTRO_MUSIC_PATH = "assets/audio/outro.mp3"

    def __init__(self, width=800, height=600):
        """
        Initialize the victory screen.

        Args:
            width: Screen width
            height: Screen height
        """
        self.width = width
        self.height = height

        # Colors
        self.bg_color = (10, 10, 20)
        self.title_color = (255, 215, 0)  # Gold
        self.credit_color = (200, 200, 200)

        # Fonts
        pygame.font.init()
        self.title_font = pygame.font.Font(None, 100)
        self.credit_font = pygame.font.Font(None, 50)
        self.name_font = pygame.font.Font(None, 40)

        # Credits
        self.credits = [
            ("Game Director", "Sarah Mitchell"),
            ("Lead Programmer", "Alex Chen"),
            ("Level Designer", "Marcus Rodriguez"),
            ("Sound Designer", "Emily Thompson"),
        ]

        # Scroll state
        self.scroll_y = height
        self.scroll_speed = 30.0  # pixels per second

        # Load outro music
        self._load_outro_music()

    def _load_outro_music(self):
        """Load and play outro music."""
        if os.path.exists(self.OUTRO_MUSIC_PATH):
            try:
                pygame.mixer.music.load(self.OUTRO_MUSIC_PATH)
                pygame.mixer.music.play(-1)  # Loop
            except Exception as e:
                print(f"Could not load outro music: {e}")

    def update(self, delta_time):
        """
        Update credits scroll.

        Args:
            delta_time: Time since last update
        """
        self.scroll_y -= self.scroll_speed * delta_time

    def handle_event(self, event):
        """
        Handle victory screen input events.

        Args:
            event: pygame event

        Returns:
            str: Action to take ('quit', 'menu', None)
        """
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE or event.key == pygame.K_RETURN:
                return 'menu'
        elif event.type == pygame.MOUSEBUTTONDOWN:
            return 'menu'

        return None

    def render(self, screen):
        """
        Render the victory screen.

        Args:
            screen: pygame surface to render to
        """
        # Background
        screen.fill(self.bg_color)

        # Victory title
        title_text = self.title_font.render("VICTORY!", True, self.title_color)
        title_x = self.width // 2 - title_text.get_width() // 2
        screen.blit(title_text, (title_x, 100))

        # Credits (scrolling)
        current_y = self.scroll_y

        for role, name in self.credits:
            # Role
            role_text = self.credit_font.render(role, True, self.credit_color)
            role_x = self.width // 2 - role_text.get_width() // 2
            if -50 < current_y < self.height + 50:  # Only render if visible
                screen.blit(role_text, (role_x, current_y))
            current_y += 60

            # Name
            name_text = self.name_font.render(name, True, self.title_color)
            name_x = self.width // 2 - name_text.get_width() // 2
            if -50 < current_y < self.height + 50:  # Only render if visible
                screen.blit(name_text, (name_x, current_y))
            current_y += 80

        # Instructions at bottom
        inst_font = pygame.font.Font(None, 30)
        inst_text = inst_font.render("Press ESC or click to return to menu", True, self.credit_color)
        screen.blit(inst_text, (self.width // 2 - inst_text.get_width() // 2, self.height - 50))
