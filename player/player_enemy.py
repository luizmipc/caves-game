from OpenGL.GL import *
from OpenGL.GLU import *
import pygame
import os
import numpy as np


class PlayerEnemy:
    """Inimigo com textura que persegue o jogador."""

    TEXTURE_PATH = "assets/textures/enemy.png"

    def __init__(self, x=0.0, y=1.7, z=0.0):
        """
        Inicializa o inimigo jogador.

        Args:
            x: Posição X
            y: Posição Y
            z: Posição Z
        """
        self.x = x
        self.y = y
        self.z = z
        self.size = 2.0  # Tamanho do billboard
        self.detection_range = 15.0  # Alcance para detectar jogador
        self.chase_speed = 3.5  # Velocidade ao perseguir
        self.is_chasing = False
        self.texture_id = self._load_texture()

    @classmethod
    def _load_texture(cls):
        """Carrega a textura do inimigo se ela existir."""
        if not os.path.exists(cls.TEXTURE_PATH):
            return None

        try:
            texture_surface = pygame.image.load(cls.TEXTURE_PATH)
            texture_surface = texture_surface.convert_alpha()

            # Inverte a textura verticalmente para o OpenGL
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
            print(f"Could not load enemy texture: {e}")
            return None

    def can_see_player(self, player_x, player_z):
        """
        Verifica se o inimigo pode ver o jogador.

        Args:
            player_x: Posição X do jogador
            player_z: Posição Z do jogador

        Returns:
            bool: True se o jogador está no alcance
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
            bool: True se o inimigo capturou o jogador (colisão detectada), False caso contrário
        """
        # Verifica se podemos ver o jogador
        if self.can_see_player(player_x, player_z):
            self.is_chasing = True

        # Persegue o jogador se avistado
        if self.is_chasing:
            dx = player_x - self.x
            dz = player_z - self.z
            distance = np.sqrt(dx * dx + dz * dz)

            # Verifica se o inimigo capturou o jogador (detecção de colisão)
            if distance < 1.0:  # Capturado dentro de 1 unidade - GAME OVER
                return True

            if distance > 0.5:  # Não se move se muito perto
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
        Renderiza o inimigo como um sprite billboard virado para o jogador.

        Args:
            player_x: Posição X do jogador para orientação do billboard
            player_z: Posição Z do jogador para orientação do billboard
        """
        glPushMatrix()

        # Move para posição
        glTranslatef(self.x, self.y, self.z)

        # Billboard: sempre virado para o jogador
        dx = player_x - self.x
        dz = player_z - self.z
        angle = np.arctan2(dx, dz) * 180.0 / np.pi
        glRotatef(-angle, 0, 1, 0)

        # Habilita transparência
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

        if self.texture_id:
            glEnable(GL_TEXTURE_2D)
            glBindTexture(GL_TEXTURE_2D, self.texture_id)
            glColor4f(1.0, 1.0, 1.0, 1.0)
        else:
            # Quadrado vermelho se não houver textura
            glColor4f(1.0, 0.0, 0.0, 1.0)

        # Desenha billboard centrado na posição
        half_size = self.size / 2
        glBegin(GL_QUADS)
        if self.texture_id:
            glTexCoord2f(0, 0)
        glVertex3f(-half_size, -half_size, 0)
        if self.texture_id:
            glTexCoord2f(1, 0)
        glVertex3f(half_size, -half_size, 0)
        if self.texture_id:
            glTexCoord2f(1, 1)
        glVertex3f(half_size, half_size, 0)
        if self.texture_id:
            glTexCoord2f(0, 1)
        glVertex3f(-half_size, half_size, 0)
        glEnd()

        if self.texture_id:
            glDisable(GL_TEXTURE_2D)

        glDisable(GL_BLEND)

        glPopMatrix()
