from OpenGL.GL import *
from .framework import PlaceElement
import pygame
import os


class Floor(PlaceElement):
    TEXTURE_PATH = "assets/textures/floor.png"

    def __init__(self, size=50.0, tile_size=1.0):
        """
        Inicializa uma grade de piso.

        Args:
            size: Tamanho total do piso (size x size)
            tile_size: Tamanho de cada bloco da grade
        """
        self.size = size
        self.tile_size = tile_size
        self.texture_id = None
        self._load_texture()

    def _load_texture(self):
        """Carrega a textura do piso se ela existir."""
        if not os.path.exists(self.TEXTURE_PATH):
            return

        try:
            texture_surface = pygame.image.load(self.TEXTURE_PATH)
            texture_surface = texture_surface.convert_alpha()

            # Inverte a textura verticalmente para o OpenGL
            texture_data = pygame.image.tostring(texture_surface, "RGBA", 1)
            width = texture_surface.get_width()
            height = texture_surface.get_height()

            self.texture_id = glGenTextures(1)
            glBindTexture(GL_TEXTURE_2D, self.texture_id)
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
            glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, width, height, 0, GL_RGBA, GL_UNSIGNED_BYTE, texture_data)
        except Exception as e:
            print(f"Could not load floor texture: {e}")
            self.texture_id = None

    def render(self):
        """Renderiza o piso como uma grade."""
        glPushMatrix()

        # Desenha a superfície principal do piso
        half_size = self.size / 2

        if self.texture_id:
            glEnable(GL_TEXTURE_2D)
            glBindTexture(GL_TEXTURE_2D, self.texture_id)
            glColor3f(1.0, 1.0, 1.0)  # Branco para mostrar a textura como está
            glBegin(GL_QUADS)
            glNormal3f(0.0, 1.0, 0.0)  # Normal apontando para cima para iluminação adequada
            glTexCoord2f(0, 0)
            glVertex3f(-half_size, 0, -half_size)
            glTexCoord2f(self.size / self.tile_size, 0)
            glVertex3f(half_size, 0, -half_size)
            glTexCoord2f(self.size / self.tile_size, self.size / self.tile_size)
            glVertex3f(half_size, 0, half_size)
            glTexCoord2f(0, self.size / self.tile_size)
            glVertex3f(-half_size, 0, half_size)
            glEnd()
            glDisable(GL_TEXTURE_2D)
        else:
            glBegin(GL_QUADS)
            glColor3f(0.3, 0.3, 0.3)  # Piso cinza escuro
            glNormal3f(0.0, 1.0, 0.0)  # Normal apontando para cima para iluminação adequada
            glVertex3f(-half_size, 0, -half_size)
            glVertex3f(half_size, 0, -half_size)
            glVertex3f(half_size, 0, half_size)
            glVertex3f(-half_size, 0, half_size)
            glEnd()

        glPopMatrix()
