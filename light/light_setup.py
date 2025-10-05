"""
Módulo de configuração de iluminação OpenGL.
Lida com toda configuração de iluminação OpenGL.
"""

from OpenGL.GL import *
import numpy as np


class LightingSetup:
    """Gerencia configuração de iluminação OpenGL."""

    @staticmethod
    def setup_global_lighting(global_ambient):
        """
        Configura parâmetros globais de iluminação.

        Args:
            global_ambient: Cor da luz ambiente global [r, g, b, a]
        """
        # Define luz ambiente global
        glLightModelfv(GL_LIGHT_MODEL_AMBIENT, global_ambient)

        # Iluminação de dois lados para que ambos os lados dos polígonos sejam iluminados
        glLightModeli(GL_LIGHT_MODEL_TWO_SIDE, GL_TRUE)

    @staticmethod
    def setup_fog(fog_color, fog_start, fog_end, fog_density):
        """
        Configura neblina para percepção de profundidade.

        Args:
            fog_color: Cor da neblina [r, g, b, a]
            fog_start: Distância onde a neblina começa
            fog_end: Distância onde a neblina é completa
            fog_density: Densidade da neblina (para neblina exponencial)
        """
        glEnable(GL_FOG)
        glFogi(GL_FOG_MODE, GL_LINEAR)  # Neblina linear para queda previsível
        glFogfv(GL_FOG_COLOR, fog_color)
        glFogf(GL_FOG_START, fog_start)
        glFogf(GL_FOG_END, fog_end)
        glHint(GL_FOG_HINT, GL_NICEST)  # Neblina de melhor qualidade

    @staticmethod
    def setup_spotlight(position, direction, cutoff_angle, exponent,
                       diffuse_color, ambient_color, specular_color,
                       constant_atten, linear_atten, quadratic_atten):
        """
        Configura parâmetros do spotlight.

        Args:
            position: Posição da luz [x, y, z, w]
            direction: Direção da luz [x, y, z]
            cutoff_angle: Ângulo do cone do spotlight em graus
            exponent: Expoente de queda do spotlight
            diffuse_color: Cor difusa [r, g, b, a]
            ambient_color: Cor ambiente [r, g, b, a]
            specular_color: Cor especular [r, g, b, a]
            constant_atten: Atenuação constante
            linear_atten: Atenuação linear
            quadratic_atten: Atenuação quadrática
        """
        # Habilita iluminação
        glEnable(GL_LIGHTING)
        glEnable(GL_LIGHT0)

        # Posiciona a luz (luz posicional)
        light_pos = np.array([position[0], position[1], position[2], 1.0], dtype=np.float32)
        glLightfv(GL_LIGHT0, GL_POSITION, light_pos)

        # Define direção do spotlight
        glLightfv(GL_LIGHT0, GL_SPOT_DIRECTION, direction)
        glLightf(GL_LIGHT0, GL_SPOT_CUTOFF, cutoff_angle)
        glLightf(GL_LIGHT0, GL_SPOT_EXPONENT, exponent)

        # Define cores da luz
        glLightfv(GL_LIGHT0, GL_DIFFUSE, diffuse_color)
        glLightfv(GL_LIGHT0, GL_AMBIENT, ambient_color)
        glLightfv(GL_LIGHT0, GL_SPECULAR, specular_color)

        # Define atenuação
        glLightf(GL_LIGHT0, GL_CONSTANT_ATTENUATION, constant_atten)
        glLightf(GL_LIGHT0, GL_LINEAR_ATTENUATION, linear_atten)
        glLightf(GL_LIGHT0, GL_QUADRATIC_ATTENUATION, quadratic_atten)

    @staticmethod
    def setup_material_properties(ambient, diffuse, specular, shininess):
        """
        Configura propriedades padrão do material.

        Args:
            ambient: Cor ambiente do material [r, g, b, a]
            diffuse: Cor difusa do material [r, g, b, a]
            specular: Cor especular do material [r, g, b, a]
            shininess: Valor de brilho do material
        """
        glMaterialfv(GL_FRONT_AND_BACK, GL_AMBIENT, ambient)
        glMaterialfv(GL_FRONT_AND_BACK, GL_DIFFUSE, diffuse)
        glMaterialfv(GL_FRONT_AND_BACK, GL_SPECULAR, specular)
        glMaterialf(GL_FRONT_AND_BACK, GL_SHININESS, shininess)

        # Habilita material de cor
        glEnable(GL_COLOR_MATERIAL)
        glColorMaterial(GL_FRONT_AND_BACK, GL_AMBIENT_AND_DIFFUSE)

        # Habilita reescalonamento automático de normais para melhor precisão de iluminação
        glEnable(GL_RESCALE_NORMAL)  # Mais eficiente que GL_NORMALIZE

        # Habilita sombreamento suave para transições graduais de luz
        glShadeModel(GL_SMOOTH)

        # Habilita visualizador local para destaques especulares mais precisos
        glLightModeli(GL_LIGHT_MODEL_LOCAL_VIEWER, GL_TRUE)

    @staticmethod
    def disable_lighting():
        """Desabilita toda iluminação."""
        glDisable(GL_LIGHTING)
        glDisable(GL_LIGHT0)
        glDisable(GL_COLOR_MATERIAL)
        glDisable(GL_NORMALIZE)
        glDisable(GL_FOG)
