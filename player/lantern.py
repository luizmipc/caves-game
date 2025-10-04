"""
Lantern module for player flashlight/torch effect.
Creates a directional light cone illuminating what's ahead of the player.
"""

from OpenGL.GL import *
import math


class Lantern:
    """Player's lantern that illuminates the area ahead."""

    def __init__(self, light_radius=15.0, cone_angle=45.0):
        """
        Initialize the lantern.

        Args:
            light_radius: Maximum distance the light reaches
            cone_angle: Angle of the light cone in degrees
        """
        self.light_radius = light_radius
        self.cone_angle = cone_angle
        self.is_on = True

    def setup(self, player_x, player_y, player_z, yaw, pitch):
        """
        Setup the lantern light based on player position and view direction.

        Args:
            player_x: Player X position
            player_y: Player Y position
            player_z: Player Z position
            yaw: Player yaw angle (horizontal rotation)
            pitch: Player pitch angle (vertical rotation)
        """
        if not self.is_on:
            return

        # Enable lighting
        glEnable(GL_LIGHTING)
        glEnable(GL_LIGHT0)

        # Position light at player position
        glLightfv(GL_LIGHT0, GL_POSITION, [player_x, player_y, player_z, 1.0])

        # Calculate direction vector from yaw and pitch
        # Convert angles to radians
        yaw_rad = math.radians(yaw)
        pitch_rad = math.radians(pitch)

        # Calculate direction (where player is looking)
        dir_x = math.sin(yaw_rad) * math.cos(pitch_rad)
        dir_y = -math.sin(pitch_rad)
        dir_z = -math.cos(yaw_rad) * math.cos(pitch_rad)

        # Set spotlight direction
        glLightfv(GL_LIGHT0, GL_SPOT_DIRECTION, [dir_x, dir_y, dir_z])

        # Spotlight properties
        glLightf(GL_LIGHT0, GL_SPOT_CUTOFF, self.cone_angle)  # Cone angle
        glLightf(GL_LIGHT0, GL_SPOT_EXPONENT, 15.0)  # Focus (higher = tighter beam)

        # Light colors - warm lantern glow
        glLightfv(GL_LIGHT0, GL_DIFFUSE, [1.0, 0.9, 0.7, 1.0])  # Warm white/yellow
        glLightfv(GL_LIGHT0, GL_AMBIENT, [0.05, 0.05, 0.05, 1.0])  # Very dim ambient
        glLightfv(GL_LIGHT0, GL_SPECULAR, [0.3, 0.3, 0.2, 1.0])

        # Attenuation - how light fades with distance
        glLightf(GL_LIGHT0, GL_CONSTANT_ATTENUATION, 1.0)
        glLightf(GL_LIGHT0, GL_LINEAR_ATTENUATION, 0.5 / self.light_radius)
        glLightf(GL_LIGHT0, GL_QUADRATIC_ATTENUATION, 1.0 / (self.light_radius * self.light_radius))

        # Enable color material so objects show their colors
        glEnable(GL_COLOR_MATERIAL)
        glColorMaterial(GL_FRONT_AND_BACK, GL_AMBIENT_AND_DIFFUSE)

        # Enable normals auto-normalization (important for lighting)
        glEnable(GL_NORMALIZE)

    def disable(self):
        """Disable the lantern light."""
        glDisable(GL_LIGHTING)
        glDisable(GL_LIGHT0)
        glDisable(GL_COLOR_MATERIAL)
        glDisable(GL_NORMALIZE)

    def toggle(self):
        """Toggle the lantern on/off."""
        self.is_on = not self.is_on
        if not self.is_on:
            self.disable()
