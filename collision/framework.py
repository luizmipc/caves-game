from abc import ABC, abstractmethod


class Collidable(ABC):
    """Abstract base class for objects that can be checked for collision."""

    @abstractmethod
    def check_collision(self, x, z, radius=0.5):
        """
        Check if a point (with radius) collides with this object.

        Args:
            x: X coordinate of the point
            z: Z coordinate of the point
            radius: Collision radius around the point

        Returns:
            bool: True if collision detected, False otherwise
        """
        pass


class CollisionFramework:
    """Framework for managing collision detection in the game."""

    def __init__(self):
        """Initialize the collision framework."""
        self.collidables = []

    def add_collidable(self, collidable):
        """
        Add a collidable object to the collision system.

        Args:
            collidable: A Collidable instance to add
        """
        if not isinstance(collidable, Collidable):
            raise TypeError("Object must inherit from Collidable")
        self.collidables.append(collidable)

    def remove_collidable(self, collidable):
        """
        Remove a collidable object from the collision system.

        Args:
            collidable: The collidable to remove
        """
        if collidable in self.collidables:
            self.collidables.remove(collidable)

    def check_collision(self, x, z, radius=0.5):
        """
        Check if a position collides with any registered collidable object.

        Args:
            x: X coordinate
            z: Z coordinate
            radius: Collision radius

        Returns:
            bool: True if collision detected, False otherwise
        """
        for collidable in self.collidables:
            if collidable.check_collision(x, z, radius):
                return True
        return False

    def get_colliding_objects(self, x, z, radius=0.5):
        """
        Get all objects that collide with the given position.

        Args:
            x: X coordinate
            z: Z coordinate
            radius: Collision radius

        Returns:
            list: List of colliding Collidable objects
        """
        colliding = []
        for collidable in self.collidables:
            if collidable.check_collision(x, z, radius):
                colliding.append(collidable)
        return colliding
