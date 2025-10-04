from .framework import PlaceFramework
from .floor import Floor


class Place:
    def __init__(self):
        """Initialize the place/environment using the framework."""
        self.framework = PlaceFramework()

        # Add floor to the place
        floor = Floor(size=50.0, tile_size=1.0)
        self.framework.add_element(floor)

    def render(self):
        """Render all elements of the place."""
        self.framework.render()
