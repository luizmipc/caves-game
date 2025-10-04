from abc import ABC, abstractmethod
from collision.framework import CollisionFramework, Collidable


class PlaceElement(ABC):
    """Abstract base class for place elements that can be rendered."""

    @abstractmethod
    def render(self):
        """Render this place element."""
        pass


class PlaceFramework:
    """Framework for managing and rendering place elements."""

    def __init__(self):
        """Initialize the place framework."""
        self.elements = []
        self.collision_framework = CollisionFramework()

    def add_element(self, element):
        """
        Add a renderable element to the place.

        Args:
            element: A PlaceElement instance to add
        """
        if not isinstance(element, PlaceElement):
            raise TypeError("Element must inherit from PlaceElement")
        self.elements.append(element)

        # If element is also collidable, add to collision framework
        if isinstance(element, Collidable):
            self.collision_framework.add_collidable(element)

    def remove_element(self, element):
        """
        Remove an element from the place.

        Args:
            element: The element to remove
        """
        if element in self.elements:
            self.elements.remove(element)

        # If element is collidable, remove from collision framework
        if isinstance(element, Collidable):
            self.collision_framework.remove_collidable(element)

    def render(self):
        """Render all elements in the place."""
        for element in self.elements:
            element.render()

    def check_collision(self, x, z, radius=0.5):
        """
        Check if a position collides with any element in the place.

        Args:
            x: X coordinate
            z: Z coordinate
            radius: Collision radius

        Returns:
            bool: True if collision detected, False otherwise
        """
        return self.collision_framework.check_collision(x, z, radius)
