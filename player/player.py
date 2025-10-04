from .camera import Camera
from .movement import Movement


class Player:
    def __init__(self, x=0.0, y=1.7, z=0.0):
        """
        Initialize player with position, camera, and movement.

        Args:
            x, y, z: Initial position (y is height, default at eye level ~1.7m)
        """
        self.x = x
        self.y = y
        self.z = z

        # Initialize camera and movement modules
        self.camera = Camera(sensitivity=0.1)
        self.movement = Movement(speed=5.0)

    def handle_mouse_motion(self, dx, dy):
        """
        Handle mouse movement for camera rotation.

        Args:
            dx: Mouse movement in x direction
            dy: Mouse movement in y direction
        """
        self.camera.handle_mouse_motion(dx, dy)

    def handle_key_down(self, key):
        """Handle key press events."""
        self.movement.handle_key_down(key)

    def handle_key_up(self, key):
        """Handle key release events."""
        self.movement.handle_key_up(key)

    def update(self, delta_time, collision_check=None):
        """
        Update player position based on movement state.

        Args:
            delta_time: Time elapsed since last frame in seconds
            collision_check: Optional function(x, z) -> bool to check collisions
        """
        position = (self.x, self.y, self.z)
        yaw = self.camera.get_yaw()
        self.x, self.y, self.z = self.movement.update(position, yaw, delta_time, collision_check)

    def get_view_matrix_rotation(self):
        """
        Get the rotation angles for applying to OpenGL view matrix.

        Returns:
            tuple: (pitch, yaw) in degrees
        """
        return self.camera.get_rotation()

    def get_position(self):
        """
        Get the player's current position.

        Returns:
            tuple: (x, y, z) position
        """
        return (self.x, self.y, self.z)
