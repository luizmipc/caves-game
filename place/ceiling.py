from OpenGL.GL import *
from .framework import PlaceElement
import pygame
import os


class Ceiling(PlaceElement):
    TEXTURE_PATH = "assets/textures/ceiling.png"

    def __init__(self, x=0.0, y=3.0, z=0.0, width=5.0, depth=0.2):
        """
        Initialize a ceiling that can be attached to walls.

        Args:
            x: X position (center of the ceiling)
            y: Y position (height of the ceiling)
            z: Z position (center of the ceiling)
            width: Width of the ceiling
            depth: Depth of the ceiling
        """
        self.x = x
        self.y = y
        self.z = z
        self.width = width
        self.depth = depth
        self.texture_id = self._load_texture()

    @classmethod
    def _load_texture(cls):
        """Load ceiling texture if it exists."""
        if not os.path.exists(cls.TEXTURE_PATH):
            return None

        try:
            texture_surface = pygame.image.load(cls.TEXTURE_PATH)
            texture_data = pygame.image.tostring(texture_surface, "RGB", True)
            width = texture_surface.get_width()
            height = texture_surface.get_height()

            texture_id = glGenTextures(1)
            glBindTexture(GL_TEXTURE_2D, texture_id)
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
            glTexImage2D(GL_TEXTURE_2D, 0, GL_RGB, width, height, 0, GL_RGB, GL_UNSIGNED_BYTE, texture_data)
            return texture_id
        except Exception as e:
            print(f"Could not load ceiling texture: {e}")
            return None

    @classmethod
    def from_wall(cls, wall, depth=5.0):
        """
        Create a ceiling attached to a wall's edge.

        Args:
            wall: Wall instance to attach ceiling to
            depth: Depth of the ceiling extending from the wall

        Returns:
            Ceiling: New ceiling positioned at the top and edge of the wall
        """
        # Position ceiling so it starts at the wall's front edge
        # Wall is centered at wall.z with depth wall.depth
        # Ceiling should start at wall.z + wall.depth/2 and extend forward
        ceiling_z = wall.z + (wall.depth / 2) + (depth / 2)

        return cls(
            x=wall.x,
            y=wall.height,
            z=ceiling_z,
            width=wall.width,
            depth=depth
        )

    def render(self):
        """Render the ceiling as a horizontal plane."""
        glPushMatrix()

        half_width = self.width / 2
        half_depth = self.depth / 2

        if self.texture_id:
            glEnable(GL_TEXTURE_2D)
            glBindTexture(GL_TEXTURE_2D, self.texture_id)
            glColor3f(1.0, 1.0, 1.0)  # White to show texture as-is
        else:
            glColor3f(0.7, 0.5, 0.3)  # Ceiling color (lighter than wall)

        glBegin(GL_QUADS)

        # Bottom face (visible from below)
        if self.texture_id:
            glTexCoord2f(0, 0)
        glVertex3f(self.x - half_width, self.y, self.z - half_depth)
        if self.texture_id:
            glTexCoord2f(1, 0)
        glVertex3f(self.x + half_width, self.y, self.z - half_depth)
        if self.texture_id:
            glTexCoord2f(1, 1)
        glVertex3f(self.x + half_width, self.y, self.z + half_depth)
        if self.texture_id:
            glTexCoord2f(0, 1)
        glVertex3f(self.x - half_width, self.y, self.z + half_depth)

        # Top face
        if self.texture_id:
            glTexCoord2f(0, 0)
        glVertex3f(self.x - half_width, self.y + 0.1, self.z - half_depth)
        if self.texture_id:
            glTexCoord2f(0, 1)
        glVertex3f(self.x - half_width, self.y + 0.1, self.z + half_depth)
        if self.texture_id:
            glTexCoord2f(1, 1)
        glVertex3f(self.x + half_width, self.y + 0.1, self.z + half_depth)
        if self.texture_id:
            glTexCoord2f(1, 0)
        glVertex3f(self.x + half_width, self.y + 0.1, self.z - half_depth)

        glEnd()

        # Draw edges for thickness
        glBegin(GL_QUADS)

        # Front edge
        if self.texture_id:
            glTexCoord2f(0, 0)
        glVertex3f(self.x - half_width, self.y, self.z + half_depth)
        if self.texture_id:
            glTexCoord2f(1, 0)
        glVertex3f(self.x + half_width, self.y, self.z + half_depth)
        if self.texture_id:
            glTexCoord2f(1, 1)
        glVertex3f(self.x + half_width, self.y + 0.1, self.z + half_depth)
        if self.texture_id:
            glTexCoord2f(0, 1)
        glVertex3f(self.x - half_width, self.y + 0.1, self.z + half_depth)

        # Back edge
        if self.texture_id:
            glTexCoord2f(0, 0)
        glVertex3f(self.x - half_width, self.y, self.z - half_depth)
        if self.texture_id:
            glTexCoord2f(0, 1)
        glVertex3f(self.x - half_width, self.y + 0.1, self.z - half_depth)
        if self.texture_id:
            glTexCoord2f(1, 1)
        glVertex3f(self.x + half_width, self.y + 0.1, self.z - half_depth)
        if self.texture_id:
            glTexCoord2f(1, 0)
        glVertex3f(self.x + half_width, self.y, self.z - half_depth)

        # Left edge
        if self.texture_id:
            glTexCoord2f(0, 0)
        glVertex3f(self.x - half_width, self.y, self.z - half_depth)
        if self.texture_id:
            glTexCoord2f(1, 0)
        glVertex3f(self.x - half_width, self.y, self.z + half_depth)
        if self.texture_id:
            glTexCoord2f(1, 1)
        glVertex3f(self.x - half_width, self.y + 0.1, self.z + half_depth)
        if self.texture_id:
            glTexCoord2f(0, 1)
        glVertex3f(self.x - half_width, self.y + 0.1, self.z - half_depth)

        # Right edge
        if self.texture_id:
            glTexCoord2f(0, 0)
        glVertex3f(self.x + half_width, self.y, self.z - half_depth)
        if self.texture_id:
            glTexCoord2f(0, 1)
        glVertex3f(self.x + half_width, self.y + 0.1, self.z - half_depth)
        if self.texture_id:
            glTexCoord2f(1, 1)
        glVertex3f(self.x + half_width, self.y + 0.1, self.z + half_depth)
        if self.texture_id:
            glTexCoord2f(1, 0)
        glVertex3f(self.x + half_width, self.y, self.z + half_depth)

        glEnd()

        if self.texture_id:
            glDisable(GL_TEXTURE_2D)

        glPopMatrix()
