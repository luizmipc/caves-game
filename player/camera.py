import pygame


class Camera:
    def __init__(self, sensitivity=0.1):
        """
        Initialize camera with rotation angles.

        Args:
            sensitivity: Mouse sensitivity for camera rotation
        """
        self.yaw = 0.0  # Horizontal rotation (left/right)
        self.pitch = 0.0  # Vertical rotation (up/down)
        self.sensitivity = sensitivity

    def handle_mouse_motion(self, dx, dy):
        """
        Handle mouse movement for camera rotation.

        Args:
            dx: Mouse movement in x direction
            dy: Mouse movement in y direction
        """
        self.yaw += dx * self.sensitivity
        self.pitch += dy * self.sensitivity

        # Clamp pitch to prevent camera flipping
        self.pitch = max(-89.0, min(89.0, self.pitch))

    def get_rotation(self):
        """
        Get the rotation angles for applying to OpenGL view matrix.

        Returns:
            tuple: (pitch, yaw) in degrees
        """
        return (self.pitch, self.yaw)

    def get_yaw(self):
        """Get the current yaw angle in degrees."""
        return self.yaw

    def get_pitch(self):
        """Get the current pitch angle in degrees."""
        return self.pitch
