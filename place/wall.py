from OpenGL.GL import *
from .framework import PlaceElement
from collision.framework import Collidable


class Wall(PlaceElement, Collidable):
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

        # Wall color
        glColor3f(0.6, 0.4, 0.2)  # Brown color

        # Draw the wall as a box
        glBegin(GL_QUADS)

        # Front face
        glVertex3f(self.x - half_width, 0, self.z + half_depth)
        glVertex3f(self.x + half_width, 0, self.z + half_depth)
        glVertex3f(self.x + half_width, self.height, self.z + half_depth)
        glVertex3f(self.x - half_width, self.height, self.z + half_depth)

        # Back face
        glVertex3f(self.x - half_width, 0, self.z - half_depth)
        glVertex3f(self.x - half_width, self.height, self.z - half_depth)
        glVertex3f(self.x + half_width, self.height, self.z - half_depth)
        glVertex3f(self.x + half_width, 0, self.z - half_depth)

        # Left face
        glVertex3f(self.x - half_width, 0, self.z - half_depth)
        glVertex3f(self.x - half_width, 0, self.z + half_depth)
        glVertex3f(self.x - half_width, self.height, self.z + half_depth)
        glVertex3f(self.x - half_width, self.height, self.z - half_depth)

        # Right face
        glVertex3f(self.x + half_width, 0, self.z - half_depth)
        glVertex3f(self.x + half_width, self.height, self.z - half_depth)
        glVertex3f(self.x + half_width, self.height, self.z + half_depth)
        glVertex3f(self.x + half_width, 0, self.z + half_depth)

        # Top face
        glVertex3f(self.x - half_width, self.height, self.z - half_depth)
        glVertex3f(self.x - half_width, self.height, self.z + half_depth)
        glVertex3f(self.x + half_width, self.height, self.z + half_depth)
        glVertex3f(self.x + half_width, self.height, self.z - half_depth)

        glEnd()

        glPopMatrix()
