from OpenGL.GL import *
from .framework import PlaceElement
import pygame
import os


class Ceiling(PlaceElement):
    TEXTURE_PATH = "assets/textures/ceiling.png"

    def __init__(self, x=0.0, y=3.0, z=0.0, width=5.0, depth=0.2):
        """
        Inicializa um teto que pode ser anexado a paredes.

        Args:
            x: Posição X (centro do teto)
            y: Posição Y (altura do teto)
            z: Posição Z (centro do teto)
            width: Largura do teto
            depth: Profundidade do teto
        """
        self.x = x
        self.y = y
        self.z = z
        self.width = width
        self.depth = depth
        self.texture_id = self._load_texture()

    @classmethod
    def _load_texture(cls):
        """Carrega textura do teto se existir."""
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
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
            glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, width, height, 0, GL_RGBA, GL_UNSIGNED_BYTE, texture_data)
            return texture_id
        except Exception as e:
            print(f"Could not load ceiling texture: {e}")
            return None

    @classmethod
    def from_wall(cls, wall, depth=5.0):
        """
        Cria um teto anexado à borda de uma parede.

        Args:
            wall: Instância de Wall para anexar o teto
            depth: Profundidade do teto estendendo-se da parede

        Returns:
            Ceiling: Novo teto posicionado no topo e na borda da parede
        """
        # Posiciona teto para que comece na borda frontal da parede
        # Parede está centrada em wall.z com profundidade wall.depth
        # Teto deve começar em wall.z + wall.depth/2 e estender para frente
        ceiling_z = wall.z + (wall.depth / 2) + (depth / 2)

        return cls(
            x=wall.x,
            y=wall.height,
            z=ceiling_z,
            width=wall.width,
            depth=depth
        )

    def render(self):
        """Renderiza o teto como um plano horizontal."""
        glPushMatrix()

        half_width = self.width / 2
        half_depth = self.depth / 2

        if self.texture_id:
            glEnable(GL_TEXTURE_2D)
            glBindTexture(GL_TEXTURE_2D, self.texture_id)
            glColor3f(1.0, 1.0, 1.0)  # Branco para mostrar textura como está
        else:
            glColor3f(0.7, 0.5, 0.3)  # Cor do teto (mais claro que a parede)

        glBegin(GL_QUADS)

        # Face inferior (visível de baixo) - normal apontando para baixo
        glNormal3f(0.0, -1.0, 0.0)
        if self.texture_id:
            glTexCoord2f(0, 0)
        glVertex3f(self.x - half_width, self.y, self.z - half_depth)
        if self.texture_id:
            glTexCoord2f(1, 0)
        glVertex3f(self.x + half_width, self.y, self.z - half_depth)
        if self.texture_id:
            glTexCoord2f(1, 1)
        glVertex3f(self.x + half_width, self.y, self.z + half_depth)
        if self.texture_id:
            glTexCoord2f(0, 1)
        glVertex3f(self.x - half_width, self.y, self.z + half_depth)

        # Face superior - normal apontando para cima
        glNormal3f(0.0, 1.0, 0.0)
        if self.texture_id:
            glTexCoord2f(0, 0)
        glVertex3f(self.x - half_width, self.y + 0.1, self.z - half_depth)
        if self.texture_id:
            glTexCoord2f(0, 1)
        glVertex3f(self.x - half_width, self.y + 0.1, self.z + half_depth)
        if self.texture_id:
            glTexCoord2f(1, 1)
        glVertex3f(self.x + half_width, self.y + 0.1, self.z + half_depth)
        if self.texture_id:
            glTexCoord2f(1, 0)
        glVertex3f(self.x + half_width, self.y + 0.1, self.z - half_depth)

        glEnd()

        # Desenha bordas para espessura
        glBegin(GL_QUADS)

        # Borda frontal - normal apontando para +Z
        glNormal3f(0.0, 0.0, 1.0)
        if self.texture_id:
            glTexCoord2f(0, 0)
        glVertex3f(self.x - half_width, self.y, self.z + half_depth)
        if self.texture_id:
            glTexCoord2f(1, 0)
        glVertex3f(self.x + half_width, self.y, self.z + half_depth)
        if self.texture_id:
            glTexCoord2f(1, 1)
        glVertex3f(self.x + half_width, self.y + 0.1, self.z + half_depth)
        if self.texture_id:
            glTexCoord2f(0, 1)
        glVertex3f(self.x - half_width, self.y + 0.1, self.z + half_depth)

        # Borda traseira - normal apontando para -Z
        glNormal3f(0.0, 0.0, -1.0)
        if self.texture_id:
            glTexCoord2f(0, 0)
        glVertex3f(self.x - half_width, self.y, self.z - half_depth)
        if self.texture_id:
            glTexCoord2f(0, 1)
        glVertex3f(self.x - half_width, self.y + 0.1, self.z - half_depth)
        if self.texture_id:
            glTexCoord2f(1, 1)
        glVertex3f(self.x + half_width, self.y + 0.1, self.z - half_depth)
        if self.texture_id:
            glTexCoord2f(1, 0)
        glVertex3f(self.x + half_width, self.y, self.z - half_depth)

        # Borda esquerda - normal apontando para -X
        glNormal3f(-1.0, 0.0, 0.0)
        if self.texture_id:
            glTexCoord2f(0, 0)
        glVertex3f(self.x - half_width, self.y, self.z - half_depth)
        if self.texture_id:
            glTexCoord2f(1, 0)
        glVertex3f(self.x - half_width, self.y, self.z + half_depth)
        if self.texture_id:
            glTexCoord2f(1, 1)
        glVertex3f(self.x - half_width, self.y + 0.1, self.z + half_depth)
        if self.texture_id:
            glTexCoord2f(0, 1)
        glVertex3f(self.x - half_width, self.y + 0.1, self.z - half_depth)

        # Borda direita - normal apontando para +X
        glNormal3f(1.0, 0.0, 0.0)
        if self.texture_id:
            glTexCoord2f(0, 0)
        glVertex3f(self.x + half_width, self.y, self.z - half_depth)
        if self.texture_id:
            glTexCoord2f(0, 1)
        glVertex3f(self.x + half_width, self.y + 0.1, self.z - half_depth)
        if self.texture_id:
            glTexCoord2f(1, 1)
        glVertex3f(self.x + half_width, self.y + 0.1, self.z + half_depth)
        if self.texture_id:
            glTexCoord2f(1, 0)
        glVertex3f(self.x + half_width, self.y, self.z + half_depth)

        glEnd()

        if self.texture_id:
            glDisable(GL_TEXTURE_2D)

        glPopMatrix()
