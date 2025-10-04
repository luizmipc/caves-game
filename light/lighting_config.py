"""
Lighting configuration module.
Centralized configuration for all lighting parameters.
"""

import numpy as np


class LightingConfig:
    """Configuration settings for the lighting system."""

    # Light ball physical properties
    DISTANCE_FROM_PLAYER = -1.2  # Behind player for hidden light source
    HEIGHT_OFFSET = -0.3  # Below eye level for better immersion (hidden from view)
    BALL_RADIUS = 0.15
    LIGHT_RANGE = 15.0

    # Spotlight properties
    SPOT_CUTOFF_ANGLE = 30.0  # degrees - wider cone for better ceiling/wall visibility
    SPOT_EXPONENT = 0.3  # Very soft edges - creates gradual transition at cone boundary
    PITCH_ANGLE_OFFSET = 0.0  # no offset - point exactly where player looks

    # Light intensity (RGB values) - warm color temperature for atmospheric scattering
    DIFFUSE_COLOR = np.array([10.0, 9.8, 9.5, 1.0], dtype=np.float32)
    AMBIENT_COLOR = np.array([3.0, 2.9, 2.7, 1.0], dtype=np.float32)  # Higher ambient for better surface visibility
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

    # Fog properties for depth perception
    FOG_ENABLED = True
    FOG_COLOR = np.array([0.0, 0.0, 0.0, 1.0], dtype=np.float32)  # Pure black fog for darkness
    FOG_DENSITY = 0.08  # Subtle density for gradual distance fade
    FOG_START = 5.0  # Start fading at 5 units
    FOG_END = 15.0  # Complete darkness at 15 units (matches light range)

    # Collision detection
    COLLISION_CHECK_RADIUS = 0.15
    MIN_DISTANCE_FROM_WALL = 0.1  # Reduced to allow closer approach to surfaces
    DISTANCE_STEP = 0.05
