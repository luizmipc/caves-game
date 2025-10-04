from OpenGL.GL import *
from .framework import PlaceElement
from collision.framework import Collidable
import pygame
import os


class Wall(PlaceElement, Collidable):
    TEXTURE_PATH = "assets/textures/wall.png"

    def __init__(self, x=0.0, z=0.0, width=5.0, height=3.0, depth=0.2):
        """
        Initialize a wall that occupies grid squares.

        Args:
            x: X position (center of the wall)
            z: Z position (center of the wall)
            width: Width of the wall (default 5.0 for 5 grid squares)
            height: Height of the wall
            depth: Depth/thickness of the wall
        """
        self.x = x
        self.z = z
        self.width = width
        self.height = height
        self.depth = depth
        self.texture_id = self._load_texture()

    @classmethod
    def _load_texture(cls):
        """Load wall texture if it exists."""
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
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
            glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, width, height, 0, GL_RGBA, GL_UNSIGNED_BYTE, texture_data)
            return texture_id
        except Exception as e:
            print(f"Could not load wall texture: {e}")
            return None

    def create_ceiling(self, depth=5.0):
        """
        Create and return a ceiling attached to this wall's edge.

        Args:
            depth: Depth of the ceiling extending from the wall

        Returns:
            Ceiling: A ceiling positioned at the top and edge of this wall
        """
        from .ceiling import Ceiling
        return Ceiling.from_wall(self, depth=depth)

    def check_collision(self, point_x, point_z, radius=0.5):
        """
        Check if a point (with radius) collides with this wall.

        Args:
            point_x: X coordinate of the point
            point_z: Z coordinate of the point
            radius: Collision radius around the point

        Returns:
            bool: True if collision detected, False otherwise
        """
        # Calculate wall boundaries
        half_width = self.width / 2
        half_depth = self.depth / 2

        min_x = self.x - half_width
        max_x = self.x + half_width
        min_z = self.z - half_depth
        max_z = self.z + half_depth

        # Find closest point on the wall to the given point
        closest_x = max(min_x, min(point_x, max_x))
        closest_z = max(min_z, min(point_z, max_z))

        # Calculate distance from point to closest point on wall
        distance_x = point_x - closest_x
        distance_z = point_z - closest_z
        distance_squared = distance_x * distance_x + distance_z * distance_z

        # Check if distance is less than radius
        return distance_squared < (radius * radius)

    def render(self):
        """Render the wall as a 3D box."""
        glPushMatrix()

        half_width = self.width / 2
        half_height = self.height / 2
        half_depth = self.depth / 2

        if self.texture_id:
            glEnable(GL_TEXTURE_2D)
            glBindTexture(GL_TEXTURE_2D, self.texture_id)
            glColor3f(1.0, 1.0, 1.0)  # White to show texture as-is
        else:
            glColor3f(0.6, 0.4, 0.2)  # Brown color

        # Draw the wall as a box
        glBegin(GL_QUADS)

        # Front face
        if self.texture_id:
            glTexCoord2f(0, 0)
        glVertex3f(self.x - half_width, 0, self.z + half_depth)
        if self.texture_id:
            glTexCoord2f(1, 0)
        glVertex3f(self.x + half_width, 0, self.z + half_depth)
        if self.texture_id:
            glTexCoord2f(1, 1)
        glVertex3f(self.x + half_width, self.height, self.z + half_depth)
        if self.texture_id:
            glTexCoord2f(0, 1)
        glVertex3f(self.x - half_width, self.height, self.z + half_depth)

        # Back face
        if self.texture_id:
            glTexCoord2f(0, 0)
        glVertex3f(self.x - half_width, 0, self.z - half_depth)
        if self.texture_id:
            glTexCoord2f(0, 1)
        glVertex3f(self.x - half_width, self.height, self.z - half_depth)
        if self.texture_id:
            glTexCoord2f(1, 1)
        glVertex3f(self.x + half_width, self.height, self.z - half_depth)
        if self.texture_id:
            glTexCoord2f(1, 0)
        glVertex3f(self.x + half_width, 0, self.z - half_depth)

        # Left face
        if self.texture_id:
            glTexCoord2f(0, 0)
        glVertex3f(self.x - half_width, 0, self.z - half_depth)
        if self.texture_id:
            glTexCoord2f(1, 0)
        glVertex3f(self.x - half_width, 0, self.z + half_depth)
        if self.texture_id:
            glTexCoord2f(1, 1)
        glVertex3f(self.x - half_width, self.height, self.z + half_depth)
        if self.texture_id:
            glTexCoord2f(0, 1)
        glVertex3f(self.x - half_width, self.height, self.z - half_depth)

        # Right face
        if self.texture_id:
            glTexCoord2f(0, 0)
        glVertex3f(self.x + half_width, 0, self.z - half_depth)
        if self.texture_id:
            glTexCoord2f(0, 1)
        glVertex3f(self.x + half_width, self.height, self.z - half_depth)
        if self.texture_id:
            glTexCoord2f(1, 1)
        glVertex3f(self.x + half_width, self.height, self.z + half_depth)
        if self.texture_id:
            glTexCoord2f(1, 0)
        glVertex3f(self.x + half_width, 0, self.z + half_depth)

        # Top face
        if self.texture_id:
            glTexCoord2f(0, 0)
        glVertex3f(self.x - half_width, self.height, self.z - half_depth)
        if self.texture_id:
            glTexCoord2f(0, 1)
        glVertex3f(self.x - half_width, self.height, self.z + half_depth)
        if self.texture_id:
            glTexCoord2f(1, 1)
        glVertex3f(self.x + half_width, self.height, self.z + half_depth)
        if self.texture_id:
            glTexCoord2f(1, 0)
        glVertex3f(self.x + half_width, self.height, self.z - half_depth)

        glEnd()

        if self.texture_id:
            glDisable(GL_TEXTURE_2D)

        glPopMatrix()
