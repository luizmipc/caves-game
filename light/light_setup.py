"""
OpenGL lighting setup module.
Handles all OpenGL lighting configuration.
"""

from OpenGL.GL import *
import numpy as np


class LightingSetup:
    """Manages OpenGL lighting setup."""

    @staticmethod
    def setup_global_lighting(global_ambient):
        """
        Setup global lighting parameters.

        Args:
            global_ambient: Global ambient light color [r, g, b, a]
        """
        # Set global ambient
        glLightModelfv(GL_LIGHT_MODEL_AMBIENT, global_ambient)

        # Two-sided lighting so both sides of polygons are lit
        glLightModeli(GL_LIGHT_MODEL_TWO_SIDE, GL_TRUE)

    @staticmethod
    def setup_fog(fog_color, fog_start, fog_end, fog_density):
        """
        Setup fog for depth perception.

        Args:
            fog_color: Fog color [r, g, b, a]
            fog_start: Distance where fog starts
            fog_end: Distance where fog is complete
            fog_density: Fog density (for exponential fog)
        """
        glEnable(GL_FOG)
        glFogi(GL_FOG_MODE, GL_LINEAR)  # Linear fog for predictable falloff
        glFogfv(GL_FOG_COLOR, fog_color)
        glFogf(GL_FOG_START, fog_start)
        glFogf(GL_FOG_END, fog_end)
        glHint(GL_FOG_HINT, GL_NICEST)  # Best quality fog

    @staticmethod
    def setup_spotlight(position, direction, cutoff_angle, exponent,
                       diffuse_color, ambient_color, specular_color,
                       constant_atten, linear_atten, quadratic_atten):
        """
        Setup spotlight parameters.

        Args:
            position: Light position [x, y, z, w]
            direction: Light direction [x, y, z]
            cutoff_angle: Spotlight cone angle in degrees
            exponent: Spotlight falloff exponent
            diffuse_color: Diffuse color [r, g, b, a]
            ambient_color: Ambient color [r, g, b, a]
            specular_color: Specular color [r, g, b, a]
            constant_atten: Constant attenuation
            linear_atten: Linear attenuation
            quadratic_atten: Quadratic attenuation
        """
        # Enable lighting
        glEnable(GL_LIGHTING)
        glEnable(GL_LIGHT0)

        # Position the light (positional light)
        light_pos = np.array([position[0], position[1], position[2], 1.0], dtype=np.float32)
        glLightfv(GL_LIGHT0, GL_POSITION, light_pos)

        # Set spotlight direction
        glLightfv(GL_LIGHT0, GL_SPOT_DIRECTION, direction)
        glLightf(GL_LIGHT0, GL_SPOT_CUTOFF, cutoff_angle)
        glLightf(GL_LIGHT0, GL_SPOT_EXPONENT, exponent)

        # Set light colors
        glLightfv(GL_LIGHT0, GL_DIFFUSE, diffuse_color)
        glLightfv(GL_LIGHT0, GL_AMBIENT, ambient_color)
        glLightfv(GL_LIGHT0, GL_SPECULAR, specular_color)

        # Set attenuation
        glLightf(GL_LIGHT0, GL_CONSTANT_ATTENUATION, constant_atten)
        glLightf(GL_LIGHT0, GL_LINEAR_ATTENUATION, linear_atten)
        glLightf(GL_LIGHT0, GL_QUADRATIC_ATTENUATION, quadratic_atten)

    @staticmethod
    def setup_material_properties(ambient, diffuse, specular, shininess):
        """
        Setup default material properties.

        Args:
            ambient: Material ambient color [r, g, b, a]
            diffuse: Material diffuse color [r, g, b, a]
            specular: Material specular color [r, g, b, a]
            shininess: Material shininess value
        """
        glMaterialfv(GL_FRONT_AND_BACK, GL_AMBIENT, ambient)
        glMaterialfv(GL_FRONT_AND_BACK, GL_DIFFUSE, diffuse)
        glMaterialfv(GL_FRONT_AND_BACK, GL_SPECULAR, specular)
        glMaterialf(GL_FRONT_AND_BACK, GL_SHININESS, shininess)

        # Enable color material
        glEnable(GL_COLOR_MATERIAL)
        glColorMaterial(GL_FRONT_AND_BACK, GL_AMBIENT_AND_DIFFUSE)

        # Enable automatic normal rescaling for better lighting accuracy
        glEnable(GL_RESCALE_NORMAL)  # More efficient than GL_NORMALIZE

        # Enable smooth shading for gradual light transitions
        glShadeModel(GL_SMOOTH)

        # Enable local viewer for more accurate specular highlights
        glLightModeli(GL_LIGHT_MODEL_LOCAL_VIEWER, GL_TRUE)

    @staticmethod
    def disable_lighting():
        """Disable all lighting."""
        glDisable(GL_LIGHTING)
        glDisable(GL_LIGHT0)
        glDisable(GL_COLOR_MATERIAL)
        glDisable(GL_NORMALIZE)
        glDisable(GL_FOG)
