from OpenGL.GL import *
from .framework import PlaceElement
import pygame
import os


class Outside(PlaceElement):
    """Outside environment with grass floor, sky, and walls."""

    GRASS_TEXTURE_PATH = "assets/textures/grass.png"
    SKY_TEXTURE_PATH = "assets/textures/sky.png"

    def __init__(self, maze_size=100.0):
        """
        Initialize the outside environment.

        Args:
            maze_size: Size of the maze to surround
        """
        self.maze_size = maze_size
        self.ground_size = maze_size * 5  # Much larger than maze
        self.sky_height = 100.0  # Sky ceiling height
        self.wall_height = self.sky_height  # Walls go all the way to sky

        self.grass_texture = self._load_texture(self.GRASS_TEXTURE_PATH)
        self.sky_texture = self._load_texture(self.SKY_TEXTURE_PATH)

    def _load_texture(self, path):
        """Load texture from file."""
        if not os.path.exists(path):
            return None

        try:
            texture_surface = pygame.image.load(path)
            texture_surface = texture_surface.convert_alpha()

            # Flip texture vertically for OpenGL
            texture_data = pygame.image.tostring(texture_surface, "RGBA", 1)
            width = texture_surface.get_width()
            height = texture_surface.get_height()

            texture_id = glGenTextures(1)
            glBindTexture(GL_TEXTURE_2D, texture_id)
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
            glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, width, height, 0, GL_RGBA, GL_UNSIGNED_BYTE, texture_data)
            return texture_id
        except Exception as e:
            print(f"Could not load texture {path}: {e}")
            return None

    def render(self):
        """Render the outside environment."""
        self._render_ground()
        self._render_sky()
        self._render_walls()

    def _render_ground(self):
        """Render the grass ground plane."""
        glPushMatrix()

        half_size = self.ground_size / 2

        if self.grass_texture:
            glEnable(GL_TEXTURE_2D)
            glBindTexture(GL_TEXTURE_2D, self.grass_texture)
            glColor3f(1.0, 1.0, 1.0)
        else:
            glColor3f(0.2, 0.6, 0.2)  # Green grass color

        # Draw ground with lots of texture repeats
        tile_repeat = 50
        glBegin(GL_QUADS)
        if self.grass_texture:
            glTexCoord2f(0, 0)
        glVertex3f(-half_size, -0.01, -half_size)
        if self.grass_texture:
            glTexCoord2f(tile_repeat, 0)
        glVertex3f(half_size, -0.01, -half_size)
        if self.grass_texture:
            glTexCoord2f(tile_repeat, tile_repeat)
        glVertex3f(half_size, -0.01, half_size)
        if self.grass_texture:
            glTexCoord2f(0, tile_repeat)
        glVertex3f(-half_size, -0.01, half_size)
        glEnd()

        if self.grass_texture:
            glDisable(GL_TEXTURE_2D)

        glPopMatrix()

    def _render_sky(self):
        """Render the sky dome/box."""
        glPushMatrix()

        half_size = self.ground_size / 2

        if self.sky_texture:
            glEnable(GL_TEXTURE_2D)
            glBindTexture(GL_TEXTURE_2D, self.sky_texture)
            glColor3f(1.0, 1.0, 1.0)
        else:
            glColor3f(0.5, 0.7, 1.0)  # Sky blue

        # Top (ceiling)
        glBegin(GL_QUADS)
        if self.sky_texture:
            glTexCoord2f(0, 0)
        glVertex3f(-half_size, self.sky_height, -half_size)
        if self.sky_texture:
            glTexCoord2f(1, 0)
        glVertex3f(half_size, self.sky_height, -half_size)
        if self.sky_texture:
            glTexCoord2f(1, 1)
        glVertex3f(half_size, self.sky_height, half_size)
        if self.sky_texture:
            glTexCoord2f(0, 1)
        glVertex3f(-half_size, self.sky_height, half_size)
        glEnd()

        if self.sky_texture:
            glDisable(GL_TEXTURE_2D)

        glPopMatrix()

    def _render_walls(self):
        """Render distant walls around the perimeter."""
        glPushMatrix()

        half_size = self.ground_size / 2

        # Use sky texture for walls or light gray
        if self.sky_texture:
            glEnable(GL_TEXTURE_2D)
            glBindTexture(GL_TEXTURE_2D, self.sky_texture)
            glColor3f(0.9, 0.9, 0.9)
        else:
            glColor3f(0.7, 0.7, 0.8)  # Light gray

        glBegin(GL_QUADS)

        # North wall
        if self.sky_texture:
            glTexCoord2f(0, 0)
        glVertex3f(-half_size, 0, -half_size)
        if self.sky_texture:
            glTexCoord2f(4, 0)
        glVertex3f(half_size, 0, -half_size)
        if self.sky_texture:
            glTexCoord2f(4, 1)
        glVertex3f(half_size, self.wall_height, -half_size)
        if self.sky_texture:
            glTexCoord2f(0, 1)
        glVertex3f(-half_size, self.wall_height, -half_size)

        # South wall
        if self.sky_texture:
            glTexCoord2f(0, 0)
        glVertex3f(-half_size, 0, half_size)
        if self.sky_texture:
            glTexCoord2f(0, 1)
        glVertex3f(-half_size, self.wall_height, half_size)
        if self.sky_texture:
            glTexCoord2f(4, 1)
        glVertex3f(half_size, self.wall_height, half_size)
        if self.sky_texture:
            glTexCoord2f(4, 0)
        glVertex3f(half_size, 0, half_size)

        # West wall
        if self.sky_texture:
            glTexCoord2f(0, 0)
        glVertex3f(-half_size, 0, -half_size)
        if self.sky_texture:
            glTexCoord2f(0, 1)
        glVertex3f(-half_size, self.wall_height, -half_size)
        if self.sky_texture:
            glTexCoord2f(4, 1)
        glVertex3f(-half_size, self.wall_height, half_size)
        if self.sky_texture:
            glTexCoord2f(4, 0)
        glVertex3f(-half_size, 0, half_size)

        # East wall
        if self.sky_texture:
            glTexCoord2f(0, 0)
        glVertex3f(half_size, 0, -half_size)
        if self.sky_texture:
            glTexCoord2f(4, 0)
        glVertex3f(half_size, 0, half_size)
        if self.sky_texture:
            glTexCoord2f(4, 1)
        glVertex3f(half_size, self.wall_height, half_size)
        if self.sky_texture:
            glTexCoord2f(0, 1)
        glVertex3f(half_size, self.wall_height, -half_size)

        glEnd()

        if self.sky_texture:
            glDisable(GL_TEXTURE_2D)

        glPopMatrix()
