from OpenGL.GL import *
from .framework import PlaceElement
import pygame
import os


class Floor(PlaceElement):
    TEXTURE_PATH = "assets/textures/floor.png"

    def __init__(self, size=50.0, tile_size=1.0):
        """
        Initialize a floor grid.

        Args:
            size: Total size of the floor (size x size)
            tile_size: Size of each grid tile
        """
        self.size = size
        self.tile_size = tile_size
        self.texture_id = None
        self._load_texture()

    def _load_texture(self):
        """Load floor texture if it exists."""
        if not os.path.exists(self.TEXTURE_PATH):
            return

        try:
            texture_surface = pygame.image.load(self.TEXTURE_PATH)
            texture_surface = texture_surface.convert_alpha()

            # Flip texture vertically for OpenGL
            texture_data = pygame.image.tostring(texture_surface, "RGBA", 1)
            width = texture_surface.get_width()
            height = texture_surface.get_height()

            self.texture_id = glGenTextures(1)
            glBindTexture(GL_TEXTURE_2D, self.texture_id)
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
            glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, width, height, 0, GL_RGBA, GL_UNSIGNED_BYTE, texture_data)
        except Exception as e:
            print(f"Could not load floor texture: {e}")
            self.texture_id = None

    def render(self):
        """Render the floor as a grid."""
        glPushMatrix()

        # Draw the main floor surface
        half_size = self.size / 2

        if self.texture_id:
            glEnable(GL_TEXTURE_2D)
            glBindTexture(GL_TEXTURE_2D, self.texture_id)
            glColor3f(1.0, 1.0, 1.0)  # White to show texture as-is
            glBegin(GL_QUADS)
            glTexCoord2f(0, 0)
            glVertex3f(-half_size, 0, -half_size)
            glTexCoord2f(self.size / self.tile_size, 0)
            glVertex3f(half_size, 0, -half_size)
            glTexCoord2f(self.size / self.tile_size, self.size / self.tile_size)
            glVertex3f(half_size, 0, half_size)
            glTexCoord2f(0, self.size / self.tile_size)
            glVertex3f(-half_size, 0, half_size)
            glEnd()
            glDisable(GL_TEXTURE_2D)
        else:
            glBegin(GL_QUADS)
            glColor3f(0.3, 0.3, 0.3)  # Dark gray floor
            glVertex3f(-half_size, 0, -half_size)
            glVertex3f(half_size, 0, -half_size)
            glVertex3f(half_size, 0, half_size)
            glVertex3f(-half_size, 0, half_size)
            glEnd()

        # Draw grid lines
        glBegin(GL_LINES)
        glColor3f(0.5, 0.5, 0.5)  # Light gray grid lines

        # Lines parallel to X axis
        z = -half_size
        while z <= half_size:
            glVertex3f(-half_size, 0.01, z)
            glVertex3f(half_size, 0.01, z)
            z += self.tile_size

        # Lines parallel to Z axis
        x = -half_size
        while x <= half_size:
            glVertex3f(x, 0.01, -half_size)
            glVertex3f(x, 0.01, half_size)
            x += self.tile_size

        glEnd()

        glPopMatrix()
