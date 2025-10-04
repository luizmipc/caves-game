from .framework import PlaceFramework
from .floor import Floor
from maze.maze import Maze


class Place:
    def __init__(self):
        """Initialize the place/environment using the framework."""
        self.framework = PlaceFramework()

        # Generate and add a random maze
        from maze.maze import Maze
        maze_grid = Maze.generate(size=5)  # size=5 creates 11x11, size=10 creates 21x21
        cell_size = 5.0

        # Calculate floor size to match maze dimensions exactly
        maze_rows = len(maze_grid)
        maze_cols = len(maze_grid[0]) if maze_grid else 0
        floor_size = max(maze_rows, maze_cols) * cell_size

        # Add floor to the place
        floor = Floor(size=floor_size, tile_size=cell_size)
        self.framework.add_element(floor)

        maze = Maze.build(maze_grid, cell_size=cell_size, wall_height=3.0)
        self.start_pos, self.end_pos = maze.add_to_framework(self.framework)

    def render(self):
        """Render all elements of the place."""
        self.framework.render()
