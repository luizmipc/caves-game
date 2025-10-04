from .wall import Wall
from .ceiling import Ceiling


class Hallway:
    def __init__(self, x=0.0, z=0.0, width=5.0, length=5.0, height=3.0):
        """
        Initialize a hallway (corridor) with side walls and ceiling.

        Args:
            x: X position (center)
            z: Z position (center of the hallway)
            width: Width of the hallway (X direction)
            length: Length of the hallway (Z direction)
            height: Height of the hallway
        """
        self.x = x
        self.z = z
        self.width = width
        self.length = length
        self.height = height

        # Create side walls (along Z direction)
        wall_thickness = 0.2
        left_x = x - width / 2 - wall_thickness / 2
        right_x = x + width / 2 + wall_thickness / 2

        # Left wall (extends along Z)
        self.wall_left = Wall(x=left_x, z=z, width=wall_thickness, height=height, depth=length)
        # Right wall (extends along Z)
        self.wall_right = Wall(x=right_x, z=z, width=wall_thickness, height=height, depth=length)

        # Ceiling spans the width and length
        from .ceiling import Ceiling
        self.ceiling = Ceiling(x=x, y=height, z=z, width=width, depth=length)

    def add_to_framework(self, framework):
        """
        Add all hallway components to a place framework.

        Args:
            framework: PlaceFramework instance to add elements to
        """
        framework.add_element(self.wall_left)
        framework.add_element(self.wall_right)
        framework.add_element(self.ceiling)

    def get_elements(self):
        """
        Get all hallway elements as a list.

        Returns:
            list: List of PlaceElement objects (walls and ceiling)
        """
        return [self.wall_left, self.wall_right, self.ceiling]
