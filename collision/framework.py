from abc import ABC, abstractmethod


class Collidable(ABC):
    """Classe base abstrata para objetos que podem ser verificados quanto a colisão."""

    @abstractmethod
    def check_collision(self, x, z, radius=0.5):
        """
        Verifica se um ponto (com raio) colide com este objeto.

        Args:
            x: Coordenada X do ponto
            z: Coordenada Z do ponto
            radius: Raio de colisão ao redor do ponto

        Returns:
            bool: True se colisão detectada, False caso contrário
        """
        pass


class CollisionFramework:
    """Framework para gerenciar detecção de colisão no jogo."""

    def __init__(self):
        """Inicializa o framework de colisão."""
        self.collidables = []

    def add_collidable(self, collidable):
        """
        Adiciona um objeto colidível ao sistema de colisão.

        Args:
            collidable: Uma instância de Collidable para adicionar
        """
        if not isinstance(collidable, Collidable):
            raise TypeError("Object must inherit from Collidable")
        self.collidables.append(collidable)

    def remove_collidable(self, collidable):
        """
        Remove um objeto colidível do sistema de colisão.

        Args:
            collidable: O colidível a remover
        """
        if collidable in self.collidables:
            self.collidables.remove(collidable)

    def check_collision(self, x, z, radius=0.5):
        """
        Verifica se uma posição colide com qualquer objeto colidível registrado.

        Args:
            x: Coordenada X
            z: Coordenada Z
            radius: Raio de colisão

        Returns:
            bool: True se colisão detectada, False caso contrário
        """
        for collidable in self.collidables:
            if collidable.check_collision(x, z, radius):
                return True
        return False

    def get_colliding_objects(self, x, z, radius=0.5):
        """
        Obtém todos os objetos que colidem com a posição fornecida.

        Args:
            x: Coordenada X
            z: Coordenada Z
            radius: Raio de colisão

        Returns:
            list: Lista de objetos Collidable em colisão
        """
        colliding = []
        for collidable in self.collidables:
            if collidable.check_collision(x, z, radius):
                colliding.append(collidable)
        return colliding
