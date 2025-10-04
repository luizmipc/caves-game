"""
Lighting configuration module.

Centralized configuration for all lighting parameters used in the game.
This module defines the torch-like light source that creates the atmospheric
dreamcore/liminal horror aesthetic.

The lighting system uses:
- Warm color temperature (like a torch or lantern)
- Spotlight cone for directed illumination
- Distance attenuation for realistic falloff
- Fog for atmospheric depth
- Material properties for surface interaction
"""

import numpy as np


class LightingConfig:
    """
    Configuration settings for the lighting system.

    All values can be adjusted to change the feel of the light.
    Current settings create a warm, torch-like atmosphere with
    realistic falloff and soft edges.
    """

    # ===== LIGHT BALL PHYSICAL PROPERTIES =====
    # Position of the light source relative to the player
    DISTANCE_FROM_PLAYER = -1.2  # Negative = behind player (hidden from view)
    HEIGHT_OFFSET = -0.3  # Negative = below eye level (prevents seeing the light ball)
    BALL_RADIUS = 0.15  # Visual size of the glowing orb (if visible)
    LIGHT_RANGE = 15.0  # Maximum distance the light reaches

    # ===== SPOTLIGHT PROPERTIES =====
    # Define the cone of light
    SPOT_CUTOFF_ANGLE = 35.0  # Cone angle in degrees (35° = wide but focused)
    SPOT_EXPONENT = 0.5  # Edge softness (lower = softer, higher = sharper)
    PITCH_ANGLE_OFFSET = 0.0  # Vertical aim offset (0 = points where player looks)

    # ===== LIGHT INTENSITY (RGB values) =====
    # Warm color temperature creates torch-like realism
    # Note: Values > 1.0 create over-bright lighting (intentional for strong illumination)
    DIFFUSE_COLOR = np.array([12.0, 11.5, 10.5, 1.0], dtype=np.float32)  # Main light (warm white/orange)
    AMBIENT_COLOR = np.array([5.0, 4.7, 4.2, 1.0], dtype=np.float32)  # Fill light (ensures visibility)
    SPECULAR_COLOR = np.array([6.5, 5.8, 4.8, 1.0], dtype=np.float32)  # Highlights (reflective surfaces)

    # Global ambient light (slight glow even in shadow)
    GLOBAL_AMBIENT = np.array([0.2, 0.2, 0.2, 1.0], dtype=np.float32)

    # ===== ATTENUATION (Light Falloff with Distance) =====
    # Formula: attenuation = 1.0 / (constant + linear*distance + quadratic*distance²)
    # Lower values = light reaches further
    CONSTANT_ATTENUATION = 0.1  # Base attenuation (brightness at source)
    LINEAR_ATTENUATION_FACTOR = 0.4  # Linear falloff rate
    QUADRATIC_ATTENUATION_FACTOR = 1.2  # Quadratic falloff (inverse-square law)

    # ===== MATERIAL PROPERTIES =====
    # How surfaces react to light
    MATERIAL_AMBIENT = np.array([0.28, 0.26, 0.23, 1.0], dtype=np.float32)  # Base surface color
    MATERIAL_DIFFUSE = np.array([0.95, 0.95, 0.95, 1.0], dtype=np.float32)  # Light absorption (0.95 = very responsive)
    MATERIAL_SPECULAR = np.array([0.5, 0.45, 0.35, 1.0], dtype=np.float32)  # Shininess color
    MATERIAL_SHININESS = 12.0  # Shininess factor (lower = broader highlights)

    # ===== BALL GLOW PROPERTIES =====
    # Visual appearance of the light ball itself (if visible)
    GLOW_CORE_COLOR = np.array([1.0, 0.95, 0.75, 1.0], dtype=np.float32)  # Center (bright warm white)
    GLOW_OUTER_COLOR = np.array([1.0, 0.85, 0.5, 0.4], dtype=np.float32)  # Edge (orange with transparency)
    GLOW_OUTER_SIZE_MULTIPLIER = 1.6  # Outer glow size relative to core

    # ===== FOG PROPERTIES =====
    # Creates atmospheric depth and distance perception
    FOG_ENABLED = True
    FOG_COLOR = np.array([0.0, 0.0, 0.0, 1.0], dtype=np.float32)  # Black fog (darkness)
    FOG_DENSITY = 0.1  # Fog thickness
    FOG_START = 4.0  # Distance where fog begins (units)
    FOG_END = 14.0  # Distance where fog is complete (units)

    # ===== COLLISION DETECTION =====
    # Parameters for light position adjustment near walls
    COLLISION_CHECK_RADIUS = 0.15  # Radius to check for wall collisions
    MIN_DISTANCE_FROM_WALL = 0.0  # Minimum distance from wall (0 = can touch walls)
    DISTANCE_STEP = 0.05  # Step size for collision checking
