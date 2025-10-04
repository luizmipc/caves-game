import pygame
from config import game_config


class ConfigScreen:
    """Configuration screen for game settings."""

    def __init__(self, width=800, height=600):
        """
        Initialize the config screen.

        Args:
            width: Screen width
            height: Screen height
        """
        self.width = width
        self.height = height

        # Colors
        self.bg_color = (20, 20, 30)
        self.title_color = (255, 255, 255)
        self.text_color = (200, 200, 200)
        self.slider_color = (100, 100, 100)
        self.slider_active_color = (255, 200, 50)
        self.button_color = (70, 70, 80)
        self.button_hover_color = (100, 100, 110)

        # Fonts
        pygame.font.init()
        self.title_font = pygame.font.Font(None, 70)
        self.label_font = pygame.font.Font(None, 40)
        self.value_font = pygame.font.Font(None, 50)
        self.button_font = pygame.font.Font(None, 50)

        # Maze size slider
        self.dragging_maze = False
        self.maze_slider_rect = pygame.Rect(250, 200, 300, 20)
        self.handle_radius = 15

        # Volume slider
        self.dragging_volume = False
        self.volume_slider_rect = pygame.Rect(250, 350, 300, 20)

        # Music toggle button
        self.music_toggle_button = pygame.Rect(250, 450, 180, 50)
        self.music_toggle_hover = False

        # Back button
        self.back_button = pygame.Rect(width // 2 - 100, height - 100, 200, 60)
        self.back_button_hover = False

    def _get_maze_size(self):
        """Get current maze size (1-10)."""
        return game_config.maze_size

    def _set_maze_size(self, value):
        """Set maze size (1-10)."""
        game_config.maze_size = max(1, min(10, value))

    def _get_maze_handle_x(self):
        """Get x position of maze slider handle."""
        value = self._get_maze_size()
        progress = (value - 1) / 9.0
        return self.maze_slider_rect.x + int(progress * self.maze_slider_rect.width)

    def _set_maze_from_mouse_x(self, mouse_x):
        """Set maze size from mouse x position."""
        x = max(self.maze_slider_rect.x, min(mouse_x, self.maze_slider_rect.x + self.maze_slider_rect.width))
        progress = (x - self.maze_slider_rect.x) / self.maze_slider_rect.width
        value = 1 + int(progress * 9)
        self._set_maze_size(value)

    def _get_volume_handle_x(self):
        """Get x position of volume slider handle."""
        progress = game_config.music_volume
        return self.volume_slider_rect.x + int(progress * self.volume_slider_rect.width)

    def _set_volume_from_mouse_x(self, mouse_x):
        """Set volume from mouse x position."""
        x = max(self.volume_slider_rect.x, min(mouse_x, self.volume_slider_rect.x + self.volume_slider_rect.width))
        progress = (x - self.volume_slider_rect.x) / self.volume_slider_rect.width
        game_config.music_volume = progress

    def handle_event(self, event):
        """
        Handle config screen input events.

        Args:
            event: pygame event

        Returns:
            str: Action to take ('back', None)
        """
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()

            # Check back button
            if self.back_button.collidepoint(mouse_pos):
                game_config.save()
                return 'back'

            # Check music toggle button
            if self.music_toggle_button.collidepoint(mouse_pos):
                game_config.music_enabled = not game_config.music_enabled
                game_config.save()

            # Check maze slider
            handle_x = self._get_maze_handle_x()
            handle_y = self.maze_slider_rect.centery
            dist = ((mouse_pos[0] - handle_x) ** 2 + (mouse_pos[1] - handle_y) ** 2) ** 0.5
            if dist <= self.handle_radius + 5:
                self.dragging_maze = True
            elif self.maze_slider_rect.collidepoint(mouse_pos):
                self._set_maze_from_mouse_x(mouse_pos[0])

            # Check volume slider
            vol_handle_x = self._get_volume_handle_x()
            vol_handle_y = self.volume_slider_rect.centery
            vol_dist = ((mouse_pos[0] - vol_handle_x) ** 2 + (mouse_pos[1] - vol_handle_y) ** 2) ** 0.5
            if vol_dist <= self.handle_radius + 5:
                self.dragging_volume = True
            elif self.volume_slider_rect.collidepoint(mouse_pos):
                self._set_volume_from_mouse_x(mouse_pos[0])

        elif event.type == pygame.MOUSEBUTTONUP:
            if self.dragging_maze or self.dragging_volume:
                self.dragging_maze = False
                self.dragging_volume = False
                game_config.save()

        elif event.type == pygame.MOUSEMOTION:
            mouse_pos = pygame.mouse.get_pos()

            # Update button hover states
            self.back_button_hover = self.back_button.collidepoint(mouse_pos)
            self.music_toggle_hover = self.music_toggle_button.collidepoint(mouse_pos)

            # Drag sliders
            if self.dragging_maze:
                self._set_maze_from_mouse_x(mouse_pos[0])
            if self.dragging_volume:
                self._set_volume_from_mouse_x(mouse_pos[0])

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                game_config.save()
                return 'back'

        return None

    def render(self, screen):
        """
        Render the config screen.

        Args:
            screen: pygame surface to render to
        """
        # Background
        screen.fill(self.bg_color)

        # Title
        title_text = self.title_font.render("SETTINGS", True, self.title_color)
        title_x = self.width // 2 - title_text.get_width() // 2
        screen.blit(title_text, (title_x, 50))

        # ===== MAZE SIZE =====
        # Maze size label
        label_text = self.label_font.render("Maze Size:", True, self.text_color)
        screen.blit(label_text, (250, 120))

        # Current maze size value
        value = self._get_maze_size()
        grid_size = 2 * value + 1
        value_text = self.label_font.render(f"{value} ({grid_size}x{grid_size})", True, self.slider_active_color)
        screen.blit(value_text, (250, 155))

        # Maze slider bar
        pygame.draw.rect(screen, self.slider_color, self.maze_slider_rect, border_radius=10)

        # Maze slider handle
        handle_x = self._get_maze_handle_x()
        handle_y = self.maze_slider_rect.centery
        handle_color = self.slider_active_color if self.dragging_maze else self.text_color
        pygame.draw.circle(screen, handle_color, (handle_x, handle_y), self.handle_radius)

        # Min/Max labels
        min_label = self.label_font.render("1", True, self.text_color)
        max_label = self.label_font.render("10", True, self.text_color)
        screen.blit(min_label, (self.maze_slider_rect.x - 30, self.maze_slider_rect.y - 5))
        screen.blit(max_label, (self.maze_slider_rect.x + self.maze_slider_rect.width + 10, self.maze_slider_rect.y - 5))

        # ===== MUSIC VOLUME =====
        # Volume label
        vol_label = self.label_font.render("Music Volume:", True, self.text_color)
        screen.blit(vol_label, (250, 280))

        # Current volume value
        vol_percent = int(game_config.music_volume * 100)
        vol_value_text = self.label_font.render(f"{vol_percent}%", True, self.slider_active_color)
        screen.blit(vol_value_text, (250, 315))

        # Volume slider bar
        pygame.draw.rect(screen, self.slider_color, self.volume_slider_rect, border_radius=10)

        # Volume slider handle
        vol_handle_x = self._get_volume_handle_x()
        vol_handle_y = self.volume_slider_rect.centery
        vol_handle_color = self.slider_active_color if self.dragging_volume else self.text_color
        pygame.draw.circle(screen, vol_handle_color, (vol_handle_x, vol_handle_y), self.handle_radius)

        # Volume min/max labels
        vol_min_label = self.label_font.render("0%", True, self.text_color)
        vol_max_label = self.label_font.render("100%", True, self.text_color)
        screen.blit(vol_min_label, (self.volume_slider_rect.x - 45, self.volume_slider_rect.y - 5))
        screen.blit(vol_max_label, (self.volume_slider_rect.x + self.volume_slider_rect.width + 10, self.volume_slider_rect.y - 5))

        # ===== MUSIC TOGGLE =====
        # Music toggle button
        toggle_color = self.button_hover_color if self.music_toggle_hover else self.button_color
        pygame.draw.rect(screen, toggle_color, self.music_toggle_button, border_radius=10)
        toggle_text = self.button_font.render("ON" if game_config.music_enabled else "OFF", True, self.slider_active_color if game_config.music_enabled else self.text_color)
        toggle_x = self.music_toggle_button.x + (self.music_toggle_button.width - toggle_text.get_width()) // 2
        toggle_y = self.music_toggle_button.y + (self.music_toggle_button.height - toggle_text.get_height()) // 2
        screen.blit(toggle_text, (toggle_x, toggle_y))

        # Music toggle label
        music_label = self.label_font.render("Music:", True, self.text_color)
        screen.blit(music_label, (250, 410))

        # ===== BACK BUTTON =====
        button_color = self.button_hover_color if self.back_button_hover else self.button_color
        pygame.draw.rect(screen, button_color, self.back_button, border_radius=10)
        back_text = self.button_font.render("BACK", True, self.text_color)
        text_x = self.back_button.x + (self.back_button.width - back_text.get_width()) // 2
        text_y = self.back_button.y + (self.back_button.height - back_text.get_height()) // 2
        screen.blit(back_text, (text_x, text_y))
