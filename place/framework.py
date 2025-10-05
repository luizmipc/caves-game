from abc import ABC, abstractmethod
from collision.framework import CollisionFramework, Collidable


class PlaceElement(ABC):
    """Classe base abstrata para elementos de cenário que podem ser renderizados."""

    @abstractmethod
    def render(self):
        """Renderiza este elemento de cenário."""
        pass


class PlaceFramework:
    """Framework para gerenciar e renderizar elementos de cenário."""

    def __init__(self):
        """Inicializa o framework de cenário."""
        self.elements = []
        self.collision_framework = CollisionFramework()

    def add_element(self, element):
        """
        Adiciona um elemento renderizável ao cenário.

        Args:
            element: Uma instância de PlaceElement para adicionar
        """
        if not isinstance(element, PlaceElement):
            raise TypeError("Element must inherit from PlaceElement")
        self.elements.append(element)

        # Se o elemento também é colidível, adiciona ao framework de colisão
        if isinstance(element, Collidable):
            self.collision_framework.add_collidable(element)

    def remove_element(self, element):
        """
        Remove um elemento do cenário.

        Args:
            element: O elemento a ser removido
        """
        if element in self.elements:
            self.elements.remove(element)

        # Se o elemento é colidível, remove do framework de colisão
        if isinstance(element, Collidable):
            self.collision_framework.remove_collidable(element)

    def render(self):
        """Renderiza todos os elementos do cenário."""
        for element in self.elements:
            element.render()

    def check_collision(self, x, z, radius=0.5):
        """
        Verifica se uma posição colide com algum elemento do cenário.

        Args:
            x: Coordenada X
            z: Coordenada Z
            radius: Raio de colisão

        Returns:
            bool: True se colisão detectada, False caso contrário
        """
        return self.collision_framework.check_collision(x, z, radius)
