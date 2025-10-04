"""
Light module for the game.
Creates a glowing ball light source that floats in front of the player.
"""

import numpy as np
from .lighting_config import LightingConfig
from .light_math import calculate_direction_vector, calculate_light_position, check_collision_and_adjust
from .light_setup import LightingSetup
from .light_renderer import LightRenderer


class LightBall:
    """A glowing ball of light that serves as the player's light source."""

    def __init__(self, distance=None, height_offset=None, radius=None, light_range=None):
        """
        Initialize the light ball.

        Args:
            distance: Distance in front of the player (optional, uses config default)
            height_offset: Height offset relative to player eye level (optional)
            radius: Visual radius of the glowing ball (optional)
            light_range: Maximum range of light illumination (optional)
        """
        self.config = LightingConfig()

        # Override config with provided values
        self.distance = distance if distance is not None else self.config.DISTANCE_FROM_PLAYER
        self.height_offset = height_offset if height_offset is not None else self.config.HEIGHT_OFFSET
        self.radius = radius if radius is not None else self.config.BALL_RADIUS
        self.light_range = light_range if light_range is not None else self.config.LIGHT_RANGE

        self.position = np.zeros(3, dtype=np.float32)

    def calculate_position(self, player_x, player_y, player_z, yaw, pitch, collision_check=None):
        """
        Calculate the light ball position based on player view direction.

        Args:
            player_x: Player X position
            player_y: Player Y position
            player_z: Player Z position
            yaw: Player yaw angle
            pitch: Player pitch angle
            collision_check: Optional collision checking function
        """
        # Player position vector
        player_pos = np.array([player_x, player_y, player_z], dtype=np.float32)

        # Calculate direction vector
        direction = calculate_direction_vector(yaw, pitch)

        # Adjust distance if collision detected
        adjusted_distance = self.distance
        if collision_check:
            adjusted_distance = check_collision_and_adjust(
                player_pos, direction, self.distance, collision_check,
                self.config.MIN_DISTANCE_FROM_WALL,
                self.config.DISTANCE_STEP,
                self.config.COLLISION_CHECK_RADIUS
            )

        # Calculate light position
        self.position = calculate_light_position(
            player_pos, direction, adjusted_distance, self.height_offset
        )

    def setup_lighting(self, player_x, player_y, player_z, yaw, pitch):
        """
        Setup OpenGL lighting from the light ball position.

        Args:
            player_x: Player X position
            player_y: Player Y position
            player_z: Player Z position
            yaw: Player yaw angle
            pitch: Player pitch angle
        """
        # Setup global lighting parameters
        LightingSetup.setup_global_lighting(self.config.GLOBAL_AMBIENT)

        # Calculate spotlight direction (with pitch offset)
        adjusted_pitch = pitch + self.config.PITCH_ANGLE_OFFSET
        direction = calculate_direction_vector(yaw, adjusted_pitch)

        # Calculate attenuation values
        linear_atten = self.config.LINEAR_ATTENUATION_FACTOR / self.light_range
        quadratic_atten = self.config.QUADRATIC_ATTENUATION_FACTOR / (self.light_range * self.light_range)

        # Setup spotlight
        LightingSetup.setup_spotlight(
            self.position, direction,
            self.config.SPOT_CUTOFF_ANGLE,
            self.config.SPOT_EXPONENT,
            self.config.DIFFUSE_COLOR,
            self.config.AMBIENT_COLOR,
            self.config.SPECULAR_COLOR,
            self.config.CONSTANT_ATTENUATION,
            linear_atten,
            quadratic_atten
        )

        # Setup material properties
        LightingSetup.setup_material_properties(
            self.config.MATERIAL_AMBIENT,
            self.config.MATERIAL_DIFFUSE,
            self.config.MATERIAL_SPECULAR,
            self.config.MATERIAL_SHININESS
        )

    def render_ball(self):
        """Render the glowing light ball itself."""
        LightRenderer.render_glowing_ball(
            self.position,
            self.radius,
            self.config.GLOW_CORE_COLOR,
            self.config.GLOW_OUTER_COLOR,
            self.config.GLOW_OUTER_SIZE_MULTIPLIER
        )

    def disable_lighting(self):
        """Disable the lighting system."""
        LightingSetup.disable_lighting()

    def update_and_render(self, player_x, player_y, player_z, yaw, pitch, collision_check=None):
        """
        Update light position and setup lighting in one call.

        Args:
            player_x: Player X position
            player_y: Player Y position
            player_z: Player Z position
            yaw: Player yaw angle
            pitch: Player pitch angle
            collision_check: Optional collision checking function
        """
        # Calculate where the light ball should be
        self.calculate_position(player_x, player_y, player_z, yaw, pitch, collision_check)

        # Setup the lighting from this position
        self.setup_lighting(player_x, player_y, player_z, yaw, pitch)

        # Render the visible glowing ball
        self.render_ball()
