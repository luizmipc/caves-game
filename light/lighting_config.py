"""
Lighting configuration module.
Centralized configuration for all lighting parameters.
"""

import numpy as np


class LightingConfig:
    """Configuration settings for the lighting system."""

    # Light ball physical properties
    DISTANCE_FROM_PLAYER = 0.8
    HEIGHT_OFFSET = -0.5
    BALL_RADIUS = 0.15
    LIGHT_RANGE = 15.0

    # Spotlight properties
    SPOT_CUTOFF_ANGLE = 25.0  # degrees
    SPOT_EXPONENT = 1.0  # soft falloff
    PITCH_ANGLE_OFFSET = -25.0  # tilt up 25 degrees

    # Light intensity (RGB values)
    DIFFUSE_COLOR = np.array([8.0, 7.8, 7.5, 1.0], dtype=np.float32)
    AMBIENT_COLOR = np.array([1.5, 1.5, 1.5, 1.0], dtype=np.float32)
    SPECULAR_COLOR = np.array([3.0, 2.9, 2.7, 1.0], dtype=np.float32)

    # Global ambient (pure darkness)
    GLOBAL_AMBIENT = np.array([0.0, 0.0, 0.0, 1.0], dtype=np.float32)

    # Attenuation (controls light falloff with distance)
    CONSTANT_ATTENUATION = 1.0
    LINEAR_ATTENUATION_FACTOR = 2.0
    QUADRATIC_ATTENUATION_FACTOR = 3.0

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
