from OpenGL.GL import *
from .framework import PlaceElement


class Ceiling(PlaceElement):
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

        # Ceiling color (lighter than wall)
        glColor3f(0.7, 0.5, 0.3)

        glBegin(GL_QUADS)

        # Bottom face (visible from below)
        glVertex3f(self.x - half_width, self.y, self.z - half_depth)
        glVertex3f(self.x + half_width, self.y, self.z - half_depth)
        glVertex3f(self.x + half_width, self.y, self.z + half_depth)
        glVertex3f(self.x - half_width, self.y, self.z + half_depth)

        # Top face
        glVertex3f(self.x - half_width, self.y + 0.1, self.z - half_depth)
        glVertex3f(self.x - half_width, self.y + 0.1, self.z + half_depth)
        glVertex3f(self.x + half_width, self.y + 0.1, self.z + half_depth)
        glVertex3f(self.x + half_width, self.y + 0.1, self.z - half_depth)

        glEnd()

        # Draw edges for thickness
        glBegin(GL_QUADS)

        # Front edge
        glVertex3f(self.x - half_width, self.y, self.z + half_depth)
        glVertex3f(self.x + half_width, self.y, self.z + half_depth)
        glVertex3f(self.x + half_width, self.y + 0.1, self.z + half_depth)
        glVertex3f(self.x - half_width, self.y + 0.1, self.z + half_depth)

        # Back edge
        glVertex3f(self.x - half_width, self.y, self.z - half_depth)
        glVertex3f(self.x - half_width, self.y + 0.1, self.z - half_depth)
        glVertex3f(self.x + half_width, self.y + 0.1, self.z - half_depth)
        glVertex3f(self.x + half_width, self.y, self.z - half_depth)

        # Left edge
        glVertex3f(self.x - half_width, self.y, self.z - half_depth)
        glVertex3f(self.x - half_width, self.y, self.z + half_depth)
        glVertex3f(self.x - half_width, self.y + 0.1, self.z + half_depth)
        glVertex3f(self.x - half_width, self.y + 0.1, self.z - half_depth)

        # Right edge
        glVertex3f(self.x + half_width, self.y, self.z - half_depth)
        glVertex3f(self.x + half_width, self.y + 0.1, self.z - half_depth)
        glVertex3f(self.x + half_width, self.y + 0.1, self.z + half_depth)
        glVertex3f(self.x + half_width, self.y, self.z + half_depth)

        glEnd()

        glPopMatrix()
