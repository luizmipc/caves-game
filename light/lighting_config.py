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
    SPOT_CUTOFF_ANGLE = 25.0  # degrees - reduced cone angle
    SPOT_EXPONENT = 0.5  # Slightly sharper edges for better defined light cone with smooth falloff
    PITCH_ANGLE_OFFSET = 0.0  # no offset - point exactly where player looks

    # Light intensity (RGB values) - enhanced warm color temperature for torch-like realism
    DIFFUSE_COLOR = np.array([12.0, 11.5, 10.5, 1.0], dtype=np.float32)  # Increased brightness for stronger impact
    AMBIENT_COLOR = np.array([4.0, 3.7, 3.2, 1.0], dtype=np.float32)  # Warmer ambient for realistic close-range glow
    SPECULAR_COLOR = np.array([5.5, 4.8, 3.9, 1.0], dtype=np.float32)  # Enhanced specular with warm highlights

    # Global ambient (higher for visibility when extremely close to surfaces)
    GLOBAL_AMBIENT = np.array([0.2, 0.2, 0.2, 1.0], dtype=np.float32)

    # Attenuation (controls light falloff with distance) - optimized for close-range functionality
    CONSTANT_ATTENUATION = 0.15  # Very low for maximum close-range brightness
    LINEAR_ATTENUATION_FACTOR = 0.5  # Reduced for smoother mid-range transitions
    QUADRATIC_ATTENUATION_FACTOR = 1.5  # Increased for more natural inverse-square law behavior

    # Material properties - optimized for realistic surface interaction
    MATERIAL_AMBIENT = np.array([0.28, 0.26, 0.23, 1.0], dtype=np.float32)  # Warmer ambient response
    MATERIAL_DIFFUSE = np.array([0.95, 0.95, 0.95, 1.0], dtype=np.float32)  # Maximum diffuse for strong light response
    MATERIAL_SPECULAR = np.array([0.5, 0.45, 0.35, 1.0], dtype=np.float32)  # Stronger warm specular highlights
    MATERIAL_SHININESS = 12.0  # Lower shininess for broader, softer highlights

    # Ball glow properties - enhanced warm gradient
    GLOW_CORE_COLOR = np.array([1.0, 0.95, 0.75, 1.0], dtype=np.float32)  # Warmer core
    GLOW_OUTER_COLOR = np.array([1.0, 0.85, 0.5, 0.4], dtype=np.float32)  # More orange outer glow
    GLOW_OUTER_SIZE_MULTIPLIER = 1.6  # Slightly larger outer glow for softer transition

    # Fog properties for depth perception
    FOG_ENABLED = True
    FOG_COLOR = np.array([0.0, 0.0, 0.0, 1.0], dtype=np.float32)  # Pure black fog for darkness
    FOG_DENSITY = 0.1  # Slightly increased for more pronounced atmospheric effect
    FOG_START = 4.0  # Start fading earlier for smoother transition
    FOG_END = 14.0  # Slightly reduced for better depth perception

    # Collision detection
    COLLISION_CHECK_RADIUS = 0.15
    MIN_DISTANCE_FROM_WALL = 0.0  # No minimum distance - light works even when touching walls
    DISTANCE_STEP = 0.05
