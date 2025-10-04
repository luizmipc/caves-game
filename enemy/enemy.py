from OpenGL.GL import *
from OpenGL.GLU import *
import pygame
import os
import numpy as np


class Enemy:
    """AI enemy that chases the player when spotted."""

    TEXTURE_PATH = "assets/textures/enemy.png"

    def __init__(self, x, y, z):
        """
        Initialize enemy.

        Args:
            x: X position
            y: Y position (height - center of sprite)
            z: Z position
        """
        self.x = x
        self.y = y
        self.z = z
        self.size = 2.0  # Enemy width (larger for visibility)
        self.height = 2.0  # Enemy height
        self.speed = 2.0  # Movement speed
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
            bool: True if enemy caught the player, False otherwise
        """
        # Check if we can see the player
        if self.can_see_player(player_x, player_z):
            self.is_chasing = True

        # Chase the player if spotted
        if self.is_chasing:
            dx = player_x - self.x
            dz = player_z - self.z
            distance = np.sqrt(dx * dx + dz * dz)

            # Check if enemy caught the player
            if distance < 1.0:  # Caught within 1 unit
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
        Render the enemy as a floating sphere.

        Args:
            player_x: Player X position (unused for sphere)
            player_z: Player Z position (unused for sphere)
        """
        glPushMatrix()

        # Move to enemy position
        glTranslatef(self.x, self.y, self.z)

        # Draw as a bright red sphere (easy to see)
        glColor3f(1.0, 0.0, 0.0)  # Bright red

        # Create sphere using GLU quadric
        quadric = gluNewQuadric()
        gluQuadricDrawStyle(quadric, GLU_FILL)
        gluSphere(quadric, 0.5, 16, 16)  # radius=0.5, segments=16
        gluDeleteQuadric(quadric)

        glPopMatrix()
