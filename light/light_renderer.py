"""
Módulo de renderização de luz.
Lida com a renderização da bola de luz brilhante.
"""

from OpenGL.GL import *
from OpenGL.GLU import *
import numpy as np


class LightRenderer:
    """Renderiza o visual da bola de luz brilhante."""

    @staticmethod
    def render_glowing_ball(position, radius, core_color, outer_color, outer_size_multiplier):
        """
        Renderiza uma bola brilhante na posição especificada.

        Args:
            position: Posição da luz [x, y, z]
            radius: Raio da bola
            core_color: Cor do brilho do núcleo [r, g, b, a]
            outer_color: Cor do brilho externo [r, g, b, a]
            outer_size_multiplier: Multiplicador de tamanho para brilho externo
        """
        glPushMatrix()

        # Move para a posição da luz
        glTranslatef(position[0], position[1], position[2])

        # Desabilita iluminação para a própria bola (para que ela brilhe)
        glDisable(GL_LIGHTING)

        # Habilita blending para efeito de brilho
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

        # Desenha o núcleo brilhante (amarelo-branco brilhante)
        glColor4fv(core_color)
        quadric = gluNewQuadric()
        gluSphere(quadric, radius, 16, 16)
        gluDeleteQuadric(quadric)

        # Desenha o brilho externo (semi-transparente)
        glColor4fv(outer_color)
        quadric = gluNewQuadric()
        gluSphere(quadric, radius * outer_size_multiplier, 16, 16)
        gluDeleteQuadric(quadric)

        glDisable(GL_BLEND)

        # Re-habilita iluminação para outros objetos
        glEnable(GL_LIGHTING)

        glPopMatrix()
