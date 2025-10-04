"""
Light renderer module.
Handles rendering of the glowing light ball.
"""

from OpenGL.GL import *
from OpenGL.GLU import *
import numpy as np


class LightRenderer:
    """Renders the glowing light ball visual."""

    @staticmethod
    def render_glowing_ball(position, radius, core_color, outer_color, outer_size_multiplier):
        """
        Render a glowing ball at the specified position.

        Args:
            position: Light position [x, y, z]
            radius: Ball radius
            core_color: Core glow color [r, g, b, a]
            outer_color: Outer glow color [r, g, b, a]
            outer_size_multiplier: Size multiplier for outer glow
        """
        glPushMatrix()

        # Move to light position
        glTranslatef(position[0], position[1], position[2])

        # Disable lighting for the ball itself (so it glows)
        glDisable(GL_LIGHTING)

        # Enable blending for glow effect
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

        # Draw the glowing core (bright yellow-white)
        glColor4fv(core_color)
        quadric = gluNewQuadric()
        gluSphere(quadric, radius, 16, 16)
        gluDeleteQuadric(quadric)

        # Draw outer glow (semi-transparent)
        glColor4fv(outer_color)
        quadric = gluNewQuadric()
        gluSphere(quadric, radius * outer_size_multiplier, 16, 16)
        gluDeleteQuadric(quadric)

        glDisable(GL_BLEND)

        # Re-enable lighting for other objects
        glEnable(GL_LIGHTING)

        glPopMatrix()
