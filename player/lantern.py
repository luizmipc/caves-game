"""
Módulo de lanterna para efeito de lanterna/tocha do jogador.
Cria um cone de luz direcional iluminando o que está à frente do jogador.
"""

from OpenGL.GL import *
import numpy as np


class Lantern:
    """Lanterna do jogador que ilumina a área à frente."""

    def __init__(self, light_radius=15.0, cone_angle=45.0):
        """
        Inicializa a lanterna.

        Args:
            light_radius: Distância máxima que a luz alcança
            cone_angle: Ângulo do cone de luz em graus
        """
        self.light_radius = light_radius
        self.cone_angle = cone_angle
        self.is_on = True

    def setup(self, player_x, player_y, player_z, yaw, pitch):
        """
        Configura a luz da lanterna com base na posição e direção de visão do jogador.

        Args:
            player_x: Posição X do jogador
            player_y: Posição Y do jogador
            player_z: Posição Z do jogador
            yaw: Ângulo yaw do jogador (rotação horizontal)
            pitch: Ângulo pitch do jogador (rotação vertical)
        """
        if not self.is_on:
            return

        # Habilita iluminação
        glEnable(GL_LIGHTING)
        glEnable(GL_LIGHT0)

        # Posiciona a luz na posição do jogador
        glLightfv(GL_LIGHT0, GL_POSITION, [player_x, player_y, player_z, 1.0])

        # Calcula vetor de direção a partir de yaw e pitch
        # Converte ângulos para radianos
        yaw_rad = np.radians(yaw)
        pitch_rad = np.radians(pitch)

        # Calcula direção (para onde o jogador está olhando)
        dir_x = np.sin(yaw_rad) * np.cos(pitch_rad)
        dir_y = -np.sin(pitch_rad)
        dir_z = -np.cos(yaw_rad) * np.cos(pitch_rad)

        # Define direção do holofote
        glLightfv(GL_LIGHT0, GL_SPOT_DIRECTION, [dir_x, dir_y, dir_z])

        # Propriedades do holofote
        glLightf(GL_LIGHT0, GL_SPOT_CUTOFF, self.cone_angle)  # Ângulo do cone
        glLightf(GL_LIGHT0, GL_SPOT_EXPONENT, 15.0)  # Foco (maior = feixe mais estreito)

        # Cores da luz - brilho quente da lanterna
        glLightfv(GL_LIGHT0, GL_DIFFUSE, [1.0, 0.9, 0.7, 1.0])  # Branco/amarelo quente
        glLightfv(GL_LIGHT0, GL_AMBIENT, [0.05, 0.05, 0.05, 1.0])  # Ambiente muito fraco
        glLightfv(GL_LIGHT0, GL_SPECULAR, [0.3, 0.3, 0.2, 1.0])

        # Atenuação - como a luz diminui com a distância
        glLightf(GL_LIGHT0, GL_CONSTANT_ATTENUATION, 1.0)
        glLightf(GL_LIGHT0, GL_LINEAR_ATTENUATION, 0.5 / self.light_radius)
        glLightf(GL_LIGHT0, GL_QUADRATIC_ATTENUATION, 1.0 / (self.light_radius * self.light_radius))

        # Habilita material colorido para que objetos mostrem suas cores
        glEnable(GL_COLOR_MATERIAL)
        glColorMaterial(GL_FRONT_AND_BACK, GL_AMBIENT_AND_DIFFUSE)

        # Habilita auto-normalização de normais (importante para iluminação)
        glEnable(GL_NORMALIZE)

    def disable(self):
        """Desabilita a luz da lanterna."""
        glDisable(GL_LIGHTING)
        glDisable(GL_LIGHT0)
        glDisable(GL_COLOR_MATERIAL)
        glDisable(GL_NORMALIZE)

    def toggle(self):
        """Alterna a lanterna ligada/desligada."""
        self.is_on = not self.is_on
        if not self.is_on:
            self.disable()
