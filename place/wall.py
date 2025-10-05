from OpenGL.GL import *
from .framework import PlaceElement
from collision.framework import Collidable
import pygame
import os


class Wall(PlaceElement, Collidable):
    TEXTURE_PATH = "assets/textures/wall.png"

    def __init__(self, x=0.0, z=0.0, width=5.0, height=3.0, depth=0.2):
        """
        Inicializa uma parede que ocupa quadrados da grade.

        Args:
            x: Posição X (centro da parede)
            z: Posição Z (centro da parede)
            width: Largura da parede (padrão 5.0 para 5 quadrados da grade)
            height: Altura da parede
            depth: Profundidade/espessura da parede
        """
        self.x = x
        self.z = z
        self.width = width
        self.height = height
        self.depth = depth
        self.texture_id = self._load_texture()

    @classmethod
    def _load_texture(cls):
        """Carrega a textura da parede se ela existir."""
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
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
            glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, width, height, 0, GL_RGBA, GL_UNSIGNED_BYTE, texture_data)
            return texture_id
        except Exception as e:
            print(f"Could not load wall texture: {e}")
            return None

    def create_ceiling(self, depth=5.0):
        """
        Cria e retorna um teto anexado à borda desta parede.

        Args:
            depth: Profundidade do teto se estendendo da parede

        Returns:
            Ceiling: Um teto posicionado no topo e borda desta parede
        """
        from .ceiling import Ceiling
        return Ceiling.from_wall(self, depth=depth)

    def check_collision(self, point_x, point_z, radius=0.5):
        """
        Verifica se um ponto (com raio) colide com esta parede.

        Args:
            point_x: Coordenada X do ponto
            point_z: Coordenada Z do ponto
            radius: Raio de colisão ao redor do ponto

        Returns:
            bool: True se colisão detectada, False caso contrário
        """
        # Calcula os limites da parede
        half_width = self.width / 2
        half_depth = self.depth / 2

        min_x = self.x - half_width
        max_x = self.x + half_width
        min_z = self.z - half_depth
        max_z = self.z + half_depth

        # Encontra o ponto mais próximo na parede do ponto dado
        closest_x = max(min_x, min(point_x, max_x))
        closest_z = max(min_z, min(point_z, max_z))

        # Calcula distância do ponto ao ponto mais próximo na parede
        distance_x = point_x - closest_x
        distance_z = point_z - closest_z
        distance_squared = distance_x * distance_x + distance_z * distance_z

        # Verifica se a distância é menor que o raio
        return distance_squared < (radius * radius)

    def render(self):
        """Renderiza a parede como uma caixa 3D."""
        glPushMatrix()

        half_width = self.width / 2
        half_height = self.height / 2
        half_depth = self.depth / 2

        if self.texture_id:
            glEnable(GL_TEXTURE_2D)
            glBindTexture(GL_TEXTURE_2D, self.texture_id)
            glColor3f(1.0, 1.0, 1.0)  # Branco para mostrar a textura como está
        else:
            glColor3f(0.6, 0.4, 0.2)  # Cor marrom

        # Desenha a parede como uma caixa com normais adequadas
        glBegin(GL_QUADS)

        # Face frontal (normal apontando para +Z)
        glNormal3f(0.0, 0.0, 1.0)
        if self.texture_id:
            glTexCoord2f(0, 0)
        glVertex3f(self.x - half_width, 0, self.z + half_depth)
        if self.texture_id:
            glTexCoord2f(1, 0)
        glVertex3f(self.x + half_width, 0, self.z + half_depth)
        if self.texture_id:
            glTexCoord2f(1, 1)
        glVertex3f(self.x + half_width, self.height, self.z + half_depth)
        if self.texture_id:
            glTexCoord2f(0, 1)
        glVertex3f(self.x - half_width, self.height, self.z + half_depth)

        # Face traseira (normal apontando para -Z)
        glNormal3f(0.0, 0.0, -1.0)
        if self.texture_id:
            glTexCoord2f(0, 0)
        glVertex3f(self.x - half_width, 0, self.z - half_depth)
        if self.texture_id:
            glTexCoord2f(0, 1)
        glVertex3f(self.x - half_width, self.height, self.z - half_depth)
        if self.texture_id:
            glTexCoord2f(1, 1)
        glVertex3f(self.x + half_width, self.height, self.z - half_depth)
        if self.texture_id:
            glTexCoord2f(1, 0)
        glVertex3f(self.x + half_width, 0, self.z - half_depth)

        # Face esquerda (normal apontando para -X)
        glNormal3f(-1.0, 0.0, 0.0)
        if self.texture_id:
            glTexCoord2f(0, 0)
        glVertex3f(self.x - half_width, 0, self.z - half_depth)
        if self.texture_id:
            glTexCoord2f(1, 0)
        glVertex3f(self.x - half_width, 0, self.z + half_depth)
        if self.texture_id:
            glTexCoord2f(1, 1)
        glVertex3f(self.x - half_width, self.height, self.z + half_depth)
        if self.texture_id:
            glTexCoord2f(0, 1)
        glVertex3f(self.x - half_width, self.height, self.z - half_depth)

        # Face direita (normal apontando para +X)
        glNormal3f(1.0, 0.0, 0.0)
        if self.texture_id:
            glTexCoord2f(0, 0)
        glVertex3f(self.x + half_width, 0, self.z - half_depth)
        if self.texture_id:
            glTexCoord2f(0, 1)
        glVertex3f(self.x + half_width, self.height, self.z - half_depth)
        if self.texture_id:
            glTexCoord2f(1, 1)
        glVertex3f(self.x + half_width, self.height, self.z + half_depth)
        if self.texture_id:
            glTexCoord2f(1, 0)
        glVertex3f(self.x + half_width, 0, self.z + half_depth)

        # Face superior (normal apontando para +Y)
        glNormal3f(0.0, 1.0, 0.0)
        if self.texture_id:
            glTexCoord2f(0, 0)
        glVertex3f(self.x - half_width, self.height, self.z - half_depth)
        if self.texture_id:
            glTexCoord2f(0, 1)
        glVertex3f(self.x - half_width, self.height, self.z + half_depth)
        if self.texture_id:
            glTexCoord2f(1, 1)
        glVertex3f(self.x + half_width, self.height, self.z + half_depth)
        if self.texture_id:
            glTexCoord2f(1, 0)
        glVertex3f(self.x + half_width, self.height, self.z - half_depth)

        glEnd()

        if self.texture_id:
            glDisable(GL_TEXTURE_2D)

        glPopMatrix()
