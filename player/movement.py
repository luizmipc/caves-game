import numpy as np
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

    def update(self, position, yaw, delta_time, collision_check=None):
        """
        Calculate new position based on movement state and camera yaw.

        Args:
            position: Current position tuple (x, y, z)
            yaw: Camera yaw angle in degrees
            delta_time: Time elapsed since last frame in seconds
            collision_check: Optional function(x, z) -> bool to check collisions

        Returns:
            tuple: New position (x, y, z)
        """
        x, y, z = position
        yaw_rad = np.radians(yaw)
        new_x, new_z = x, z

        # Forward/backward movement
        if self.moving_forward:
            new_x += np.sin(yaw_rad) * self.speed * delta_time
            new_z -= np.cos(yaw_rad) * self.speed * delta_time
        if self.moving_backward:
            new_x -= np.sin(yaw_rad) * self.speed * delta_time
            new_z += np.cos(yaw_rad) * self.speed * delta_time

        # Strafe left/right movement
        if self.moving_left:
            new_x -= np.cos(yaw_rad) * self.speed * delta_time
            new_z -= np.sin(yaw_rad) * self.speed * delta_time
        if self.moving_right:
            new_x += np.cos(yaw_rad) * self.speed * delta_time
            new_z += np.sin(yaw_rad) * self.speed * delta_time

        # Check collision before applying movement
        if collision_check is None or not collision_check(new_x, new_z):
            x, z = new_x, new_z

        return (x, y, z)
