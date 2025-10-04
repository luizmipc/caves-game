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
    SPOT_EXPONENT = 0.3  # Very soft edges - creates gradual transition at cone boundary
    PITCH_ANGLE_OFFSET = 0.0  # no offset - point exactly where player looks

    # Light intensity (RGB values) - warm color temperature for atmospheric scattering
    DIFFUSE_COLOR = np.array([10.0, 9.8, 9.5, 1.0], dtype=np.float32)
    AMBIENT_COLOR = np.array([2.2, 2.1, 1.9, 1.0], dtype=np.float32)  # Subtle warm glow for scattered light
    SPECULAR_COLOR = np.array([5.0, 4.5, 3.8, 1.0], dtype=np.float32)  # Enhanced specular for light scattering effect

    # Global ambient (slight glow around light to illuminate very close surfaces)
    GLOBAL_AMBIENT = np.array([0.1, 0.1, 0.1, 1.0], dtype=np.float32)

    # Attenuation (controls light falloff with distance) - optimized for smooth, realistic falloff
    CONSTANT_ATTENUATION = 0.25  # Even lower for broader light spread at source
    LINEAR_ATTENUATION_FACTOR = 0.6  # Reduced for smoother mid-range transitions
    QUADRATIC_ATTENUATION_FACTOR = 1.5  # Increased for more natural inverse-square law behavior

    # Material properties - adjusted for light scattering
    MATERIAL_AMBIENT = np.array([0.25, 0.24, 0.22, 1.0], dtype=np.float32)  # Slight warm tint
    MATERIAL_DIFFUSE = np.array([0.8, 0.8, 0.8, 1.0], dtype=np.float32)
    MATERIAL_SPECULAR = np.array([0.4, 0.35, 0.3, 1.0], dtype=np.float32)  # Enhanced for scattering glow
    MATERIAL_SHININESS = 15.0  # Lower shininess for softer, more scattered highlights

    # Ball glow properties
    GLOW_CORE_COLOR = np.array([1.0, 1.0, 0.8, 1.0], dtype=np.float32)
    GLOW_OUTER_COLOR = np.array([1.0, 0.9, 0.6, 0.3], dtype=np.float32)
    GLOW_OUTER_SIZE_MULTIPLIER = 1.5

    # Collision detection
    COLLISION_CHECK_RADIUS = 0.2
    MIN_DISTANCE_FROM_WALL = 0.3
    DISTANCE_STEP = 0.1
