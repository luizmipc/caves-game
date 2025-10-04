"""
Lighting configuration module.
Centralized configuration for all lighting parameters.
"""

import numpy as np


class LightingConfig:
    """Configuration settings for the lighting system."""

    # Light ball physical properties
    DISTANCE_FROM_PLAYER = 0.2  # Very close to player, almost inside
    HEIGHT_OFFSET = 0.0  # At eye level
    BALL_RADIUS = 0.15
    LIGHT_RANGE = 15.0

    # Spotlight properties
    SPOT_CUTOFF_ANGLE = 20.0  # degrees
    SPOT_EXPONENT = 0.5  # very soft falloff for better spread
    PITCH_ANGLE_OFFSET = 0.0  # no offset - point exactly where player looks

    # Light intensity (RGB values)
    DIFFUSE_COLOR = np.array([10.0, 9.8, 9.5, 1.0], dtype=np.float32)
    AMBIENT_COLOR = np.array([2.0, 2.0, 2.0, 1.0], dtype=np.float32)  # High ambient for close surfaces
    SPECULAR_COLOR = np.array([4.0, 3.9, 3.7, 1.0], dtype=np.float32)

    # Global ambient (slight glow around light to illuminate very close surfaces)
    GLOBAL_AMBIENT = np.array([0.1, 0.1, 0.1, 1.0], dtype=np.float32)

    # Attenuation (controls light falloff with distance) - reduced for better close-range illumination
    CONSTANT_ATTENUATION = 0.5
    LINEAR_ATTENUATION_FACTOR = 1.0
    QUADRATIC_ATTENUATION_FACTOR = 1.5

    # Material properties
    MATERIAL_AMBIENT = np.array([0.2, 0.2, 0.2, 1.0], dtype=np.float32)
    MATERIAL_DIFFUSE = np.array([0.8, 0.8, 0.8, 1.0], dtype=np.float32)
    MATERIAL_SPECULAR = np.array([0.3, 0.3, 0.3, 1.0], dtype=np.float32)
    MATERIAL_SHININESS = 20.0

    # Ball glow properties
    GLOW_CORE_COLOR = np.array([1.0, 1.0, 0.8, 1.0], dtype=np.float32)
    GLOW_OUTER_COLOR = np.array([1.0, 0.9, 0.6, 0.3], dtype=np.float32)
    GLOW_OUTER_SIZE_MULTIPLIER = 1.5

    # Collision detection
    COLLISION_CHECK_RADIUS = 0.2
    MIN_DISTANCE_FROM_WALL = 0.3
    DISTANCE_STEP = 0.1
