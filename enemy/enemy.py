from OpenGL.GL import *
from OpenGL.GLU import *
import pygame
import os
import numpy as np


class Enemy:
    """Inimigo IA que persegue o jogador quando avistado."""

    TEXTURE_PATH = "assets/textures/enemy.png"

    def __init__(self, x, y, z):
        """
        Inicializa inimigo.

        Args:
            x: Posição X
            y: Posição Y (altura - centro do sprite)
            z: Posição Z
        """
        self.x = x
        self.y = y
        self.z = z
        self.size = 2.0  # Largura do inimigo (maior para visibilidade)
        self.height = 2.0  # Altura do inimigo
        self.speed = 2.0  # Velocidade de movimento
        self.detection_range = 15.0  # Alcance para detectar jogador
        self.chase_speed = 3.5  # Velocidade ao perseguir
        self.is_chasing = False
        self.texture_id = self._load_texture()

    @classmethod
    def _load_texture(cls):
        """Carrega textura do inimigo se existir."""
        if not os.path.exists(cls.TEXTURE_PATH):
            return None

        try:
            texture_surface = pygame.image.load(cls.TEXTURE_PATH)
            texture_surface = texture_surface.convert_alpha()

            # Inverte textura verticalmente para OpenGL
            texture_data = pygame.image.tostring(texture_surface, "RGBA", 1)
            width = texture_surface.get_width()
            height = texture_surface.get_height()

            texture_id = glGenTextures(1)
            glBindTexture(GL_TEXTURE_2D, texture_id)
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_CLAMP)
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_CLAMP)
            glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, width, height, 0, GL_RGBA, GL_UNSIGNED_BYTE, texture_data)
            return texture_id
        except Exception as e:
            print(f"Não foi possível carregar textura do inimigo: {e}")
            return None

    def can_see_player(self, player_x, player_z):
        """
        Verifica se inimigo pode ver o jogador.

        Args:
            player_x: Posição X do jogador
            player_z: Posição Z do jogador

        Returns:
            bool: True se jogador está no alcance
        """
        dx = player_x - self.x
        dz = player_z - self.z
        distance = np.sqrt(dx * dx + dz * dz)
        return distance <= self.detection_range

    def update(self, delta_time, player_x, player_z, collision_check=None):
        """
        Atualiza IA e movimento do inimigo.

        Args:
            delta_time: Tempo desde a última atualização
            player_x: Posição X do jogador
            player_z: Posição Z do jogador
            collision_check: Função de verificação de colisão

        Returns:
            bool: True se inimigo capturou o jogador, False caso contrário
        """
        # Verifica se podemos ver o jogador
        if self.can_see_player(player_x, player_z):
            self.is_chasing = True

        # Persegue o jogador se avistado
        if self.is_chasing:
            dx = player_x - self.x
            dz = player_z - self.z
            distance = np.sqrt(dx * dx + dz * dz)

            # Verifica se inimigo capturou o jogador
            if distance < 1.0:  # Capturado dentro de 1 unidade
                return True

            if distance > 0.5:  # Não move se muito próximo
                # Normaliza direção
                dx /= distance
                dz /= distance

                # Calcula nova posição
                move_speed = self.chase_speed * delta_time
                new_x = self.x + dx * move_speed
                new_z = self.z + dz * move_speed

                # Verifica colisão com raio menor para inimigo (0.3 ao invés de 0.5 padrão)
                if collision_check is None or not collision_check(new_x, new_z, radius=0.3):
                    self.x = new_x
                    self.z = new_z

        return False

    def render(self, player_x, player_z):
        """
        Renderiza o inimigo como uma esfera flutuante.

        Args:
            player_x: Posição X do jogador (não usado para esfera)
            player_z: Posição Z do jogador (não usado para esfera)
        """
        glPushMatrix()

        # Move para posição do inimigo
        glTranslatef(self.x, self.y, self.z)

        # Desenha como uma esfera vermelha brilhante (fácil de ver)
        glColor3f(1.0, 0.0, 0.0)  # Vermelho brilhante

        # Cria esfera usando quadric GLU
        quadric = gluNewQuadric()
        gluQuadricDrawStyle(quadric, GLU_FILL)
        gluSphere(quadric, 0.5, 16, 16)  # raio=0.5, segmentos=16
        gluDeleteQuadric(quadric)

        glPopMatrix()
