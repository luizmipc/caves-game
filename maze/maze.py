from .framework import MazeFramework
from .generator import MazeGenerator


class Maze:
    """
    Maze generation and building utilities.

    Grid symbols:
    - '.' or ' ' = walkable corridor
    - '#' = solid wall block
    - 'S' = start position (walkable)
    - 'E' = end position (walkable)
    """

    @staticmethod
    def generate(size=5, algorithm='prim'):
        """
        Generate a random square maze.

        Args:
            size: Size parameter (creates (2*size+1) x (2*size+1) grid)
                 size=3 -> 7x7, size=5 -> 11x11, size=10 -> 21x21
            algorithm: 'prim' (default, better branching) or 'backtracking' (long corridors)

        Returns:
            list: 2D grid ready for MazeFramework
        """
        return MazeGenerator.generate(size, algorithm)

    @staticmethod
    def generate_rectangular(width=5, height=5, algorithm='prim'):
        """
        Generate a random rectangular maze.

        Args:
            width: Width in cells
            height: Height in cells
            algorithm: 'prim' (default, better branching) or 'backtracking' (long corridors)

        Returns:
            list: 2D grid ready for MazeFramework
        """
        return MazeGenerator.generate_rectangular(width, height, algorithm)

    @staticmethod
    def build(grid, cell_size=5.0, wall_height=3.0):
        """
        Build a maze from a grid layout.

        Args:
            grid: 2D list representing maze layout
            cell_size: Size of each grid cell
            wall_height: Height of walls

        Returns:
            MazeFramework: Framework instance ready to add to place
        """
        return MazeFramework(grid, cell_size, wall_height)

    @staticmethod
    def custom(layout_string):
        """
        Build a maze from a multiline string for easier visualization.

        Args:
            layout_string: Multiline string representing the maze

        Returns:
            list: 2D grid ready for MazeFramework

        Example:
            maze_grid = Maze.custom('''
                #######
                #S...E#
                #######
            ''')
        """
        lines = layout_string.strip().split('\n')
        grid = []
        for line in lines:
            line = line.strip()
            if line:
                grid.append(list(line))
        return grid
