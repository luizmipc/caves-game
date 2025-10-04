import math
import pygame


class Movement:
    def __init__(self, speed=5.0):
        """
        Initialize movement controller.

        Args:
            speed: Movement speed in units per second
        """
        self.speed = speed

        # Movement state
        self.moving_forward = False
        self.moving_backward = False
        self.moving_left = False
        self.moving_right = False

    def handle_key_down(self, key):
        """Handle key press events."""
        if key == pygame.K_w:
            self.moving_forward = True
        elif key == pygame.K_s:
            self.moving_backward = True
        elif key == pygame.K_a:
            self.moving_left = True
        elif key == pygame.K_d:
            self.moving_right = True

    def handle_key_up(self, key):
        """Handle key release events."""
        if key == pygame.K_w:
            self.moving_forward = False
        elif key == pygame.K_s:
            self.moving_backward = False
        elif key == pygame.K_a:
            self.moving_left = False
        elif key == pygame.K_d:
            self.moving_right = False

    def update(self, position, yaw, delta_time):
        """
        Calculate new position based on movement state and camera yaw.

        Args:
            position: Current position tuple (x, y, z)
            yaw: Camera yaw angle in degrees
            delta_time: Time elapsed since last frame in seconds

        Returns:
            tuple: New position (x, y, z)
        """
        x, y, z = position
        yaw_rad = math.radians(yaw)

        # Forward/backward movement
        if self.moving_forward:
            x += math.sin(yaw_rad) * self.speed * delta_time
            z -= math.cos(yaw_rad) * self.speed * delta_time
        if self.moving_backward:
            x -= math.sin(yaw_rad) * self.speed * delta_time
            z += math.cos(yaw_rad) * self.speed * delta_time

        # Strafe left/right movement
        if self.moving_left:
            x -= math.cos(yaw_rad) * self.speed * delta_time
            z -= math.sin(yaw_rad) * self.speed * delta_time
        if self.moving_right:
            x += math.cos(yaw_rad) * self.speed * delta_time
            z += math.sin(yaw_rad) * self.speed * delta_time

        return (x, y, z)
