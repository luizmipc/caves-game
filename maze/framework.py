"""
Maze Framework for building mazes from grid layouts.

Grid symbols:
- ' ' or '.' = walkable corridor (creates hallway segments)
- '#' = solid wall block
- 'S' = start position (walkable)
- 'E' = end position (walkable)
"""


class MazeFramework:
    """Framework for building mazes from ASCII grid layouts."""

    def __init__(self, grid, cell_size=5.0, wall_height=3.0):
        """
        Initialize maze framework.

        Args:
            grid: 2D list of strings representing the maze layout
            cell_size: Size of each grid cell (width/length)
            wall_height: Height of walls and hallways
        """
        self.grid = grid
        self.cell_size = cell_size
        self.wall_height = wall_height
        self.rows = len(grid)
        self.cols = len(grid[0]) if grid else 0

    def get_world_position(self, row, col):
        """
        Convert grid position to world coordinates.

        Args:
            row: Grid row
            col: Grid column

        Returns:
            tuple: (x, z) world position
        """
        # Center the maze at origin
        x = (col - self.cols / 2) * self.cell_size
        z = (row - self.rows / 2) * self.cell_size
        return (x, z)

    def is_walkable(self, cell):
        """Check if a cell is walkable."""
        return cell in ['.', ' ', 'S', 'E']

    def parse(self):
        """
        Parse the grid and create walls/ceiling for the maze.

        Returns:
            dict: Dictionary with 'walls', 'ceiling', 'start', 'end' positions
        """
        from place.wall import Wall
        from place.ceiling import Ceiling

        walls = []
        start_pos = None
        end_pos = None
        ceiling = None

        # Find maze bounds for ceiling
        min_x = min_z = float('inf')
        max_x = max_z = float('-inf')

        # First pass: find bounds and mark positions
        for row in range(self.rows):
            for col in range(self.cols):
                cell = self.grid[row][col]
                x, z = self.get_world_position(row, col)

                if self.is_walkable(cell):
                    min_x = min(min_x, x)
                    max_x = max(max_x, x)
                    min_z = min(min_z, z)
                    max_z = max(max_z, z)

                    if cell == 'S':
                        start_pos = (x, 1.7, z)
                    elif cell == 'E':
                        end_pos = (x, 1.7, z)

                elif cell == '#':
                    # Create wall blocks for solid walls
                    wall = Wall(
                        x=x, z=z,
                        width=self.cell_size,
                        height=self.wall_height,
                        depth=self.cell_size
                    )
                    walls.append(wall)

        # Create one large ceiling over all walkable areas
        if min_x != float('inf'):
            ceiling_x = (min_x + max_x) / 2
            ceiling_z = (min_z + max_z) / 2
            ceiling_width = (max_x - min_x) + self.cell_size
            ceiling_depth = (max_z - min_z) + self.cell_size

            ceiling = Ceiling(
                x=ceiling_x,
                y=self.wall_height,
                z=ceiling_z,
                width=ceiling_width,
                depth=ceiling_depth
            )

        return {
            'walls': walls,
            'ceiling': ceiling,
            'start': start_pos,
            'end': end_pos
        }

    def add_to_framework(self, place_framework):
        """
        Add all maze elements to a place framework.

        Args:
            place_framework: PlaceFramework instance to add elements to
        """
        elements = self.parse()

        for wall in elements['walls']:
            place_framework.add_element(wall)

        if elements['ceiling']:
            place_framework.add_element(elements['ceiling'])

        return elements['start'], elements['end']
