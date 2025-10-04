from OpenGL.GL import *
from .framework import PlaceElement


class Floor(PlaceElement):
    def __init__(self, size=50.0, tile_size=1.0):
        """
        Initialize a floor grid.

        Args:
            size: Total size of the floor (size x size)
            tile_size: Size of each grid tile
        """
        self.size = size
        self.tile_size = tile_size

    def render(self):
        """Render the floor as a grid."""
        glPushMatrix()

        # Draw the main floor surface
        glBegin(GL_QUADS)
        glColor3f(0.3, 0.3, 0.3)  # Dark gray floor
        half_size = self.size / 2
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
