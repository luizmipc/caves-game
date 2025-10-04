from abc import ABC, abstractmethod


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

    def add_element(self, element):
        """
        Add a renderable element to the place.

        Args:
            element: A PlaceElement instance to add
        """
        if not isinstance(element, PlaceElement):
            raise TypeError("Element must inherit from PlaceElement")
        self.elements.append(element)

    def remove_element(self, element):
        """
        Remove an element from the place.

        Args:
            element: The element to remove
        """
        if element in self.elements:
            self.elements.remove(element)

    def render(self):
        """Render all elements in the place."""
        for element in self.elements:
            element.render()
