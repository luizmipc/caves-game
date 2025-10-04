from OpenGL.GL import *
from OpenGL.GLU import *
import pygame
import os
import numpy as np


class PlayerEnemy:
    """Enemy with texture that chases the player."""

    TEXTURE_PATH = "assets/textures/enemy.png"

    def __init__(self, x=0.0, y=1.7, z=0.0):
        """
        Initialize player enemy.

        Args:
            x: X position
            y: Y position
            z: Z position
        """
        self.x = x
        self.y = y
        self.z = z
        self.size = 2.0  # Billboard size
        self.detection_range = 15.0  # Range to detect player
        self.chase_speed = 3.5  # Speed when chasing
        self.is_chasing = False
        self.texture_id = self._load_texture()

    @classmethod
    def _load_texture(cls):
        """Load enemy texture if it exists."""
        if not os.path.exists(cls.TEXTURE_PATH):
            return None

        try:
            texture_surface = pygame.image.load(cls.TEXTURE_PATH)
            texture_surface = texture_surface.convert_alpha()

            # Flip texture vertically for OpenGL
            texture_data = pygame.image.tostring(texture_surface, "RGBA", 1)
            width = texture_surface.get_width()
            height = texture_surface.get_height()

            texture_id = glGenTextures(1)
            glBindTexture(GL_TEXTURE_2D, texture_id)
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP)
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP)
            glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, width, height, 0, GL_RGBA, GL_UNSIGNED_BYTE, texture_data)
            return texture_id
        except Exception as e:
            print(f"Could not load enemy texture: {e}")
            return None

    def can_see_player(self, player_x, player_z):
        """
        Check if enemy can see the player.

        Args:
            player_x: Player X position
            player_z: Player Z position

        Returns:
            bool: True if player is in range
        """
        dx = player_x - self.x
        dz = player_z - self.z
        distance = np.sqrt(dx * dx + dz * dz)
        return distance <= self.detection_range

    def update(self, delta_time, player_x, player_z, collision_check=None):
        """
        Update enemy AI and movement.

        Args:
            delta_time: Time since last update
            player_x: Player X position
            player_z: Player Z position
            collision_check: Collision checking function

        Returns:
            bool: True if enemy caught the player (collision detected), False otherwise
        """
        # Check if we can see the player
        if self.can_see_player(player_x, player_z):
            self.is_chasing = True

        # Chase the player if spotted
        if self.is_chasing:
            dx = player_x - self.x
            dz = player_z - self.z
            distance = np.sqrt(dx * dx + dz * dz)

            # Check if enemy caught the player (collision detection)
            if distance < 1.0:  # Caught within 1 unit - GAME OVER
                return True

            if distance > 0.5:  # Don't move if too close
                # Normalize direction
                dx /= distance
                dz /= distance

                # Calculate new position
                move_speed = self.chase_speed * delta_time
                new_x = self.x + dx * move_speed
                new_z = self.z + dz * move_speed

                # Check collision with smaller radius for enemy (0.3 instead of default 0.5)
                if collision_check is None or not collision_check(new_x, new_z, radius=0.3):
                    self.x = new_x
                    self.z = new_z

        return False

    def render(self, player_x, player_z):
        """
        Render the enemy as a billboard sprite facing the player.

        Args:
            player_x: Player X position for billboard orientation
            player_z: Player Z position for billboard orientation
        """
        glPushMatrix()

        # Move to position
        glTranslatef(self.x, self.y, self.z)

        # Billboard: always face the player
        dx = player_x - self.x
        dz = player_z - self.z
        angle = np.arctan2(dx, dz) * 180.0 / np.pi
        glRotatef(-angle, 0, 1, 0)

        # Enable transparency
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

        if self.texture_id:
            glEnable(GL_TEXTURE_2D)
            glBindTexture(GL_TEXTURE_2D, self.texture_id)
            glColor4f(1.0, 1.0, 1.0, 1.0)
        else:
            # Red square if no texture
            glColor4f(1.0, 0.0, 0.0, 1.0)

        # Draw billboard centered at position
        half_size = self.size / 2
        glBegin(GL_QUADS)
        if self.texture_id:
            glTexCoord2f(0, 0)
        glVertex3f(-half_size, -half_size, 0)
        if self.texture_id:
            glTexCoord2f(1, 0)
        glVertex3f(half_size, -half_size, 0)
        if self.texture_id:
            glTexCoord2f(1, 1)
        glVertex3f(half_size, half_size, 0)
        if self.texture_id:
            glTexCoord2f(0, 1)
        glVertex3f(-half_size, half_size, 0)
        glEnd()

        if self.texture_id:
            glDisable(GL_TEXTURE_2D)

        glDisable(GL_BLEND)

        glPopMatrix()
