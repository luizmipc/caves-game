import random


class MazeGenerator:
    """Generate mazes using various algorithms."""

    @staticmethod
    def generate(size=5, algorithm='prim'):
        """
        Generate a square maze using specified algorithm.

        Args:
            size: Size of the maze (will create a (2*size+1) x (2*size+1) grid)
            algorithm: 'prim' (default) or 'backtracking'

        Returns:
            list: 2D grid representing the maze with '#' walls and '.' paths
        """
        if algorithm == 'prim':
            return MazeGenerator._generate_prim(size)
        else:
            return MazeGenerator._generate_backtracking(size)

    @staticmethod
    def _generate_prim(size):
        """
        Generate maze using Randomized Prim's algorithm.
        Creates mazes with better branching and less predictable paths.
        """
        grid_size = 2 * size + 1
        grid = [['#' for _ in range(grid_size)] for _ in range(grid_size)]

        # Start from random position
        start_row, start_col = 1, 1
        grid[start_row][start_col] = 'S'

        # Walls list - walls adjacent to visited cells
        walls = []
        visited = set()
        visited.add((start_row, start_col))

        # Add initial walls
        directions = [(-2, 0), (0, 2), (2, 0), (0, -2)]
        for dr, dc in directions:
            wall_row, wall_col = start_row + dr // 2, start_col + dc // 2
            new_row, new_col = start_row + dr, start_col + dc
            if 0 < new_row < grid_size - 1 and 0 < new_col < grid_size - 1:
                walls.append((wall_row, wall_col, new_row, new_col))

        while walls:
            # Pick random wall
            wall_row, wall_col, cell_row, cell_col = walls.pop(random.randrange(len(walls)))

            # If the cell on the other side hasn't been visited
            if (cell_row, cell_col) not in visited:
                # Make the wall a passage and mark the cell as visited
                grid[wall_row][wall_col] = '.'
                grid[cell_row][cell_col] = '.'
                visited.add((cell_row, cell_col))

                # Add neighboring walls of the cell
                for dr, dc in directions:
                    wall_r, wall_c = cell_row + dr // 2, cell_col + dc // 2
                    new_r, new_c = cell_row + dr, cell_col + dc
                    if (0 < new_r < grid_size - 1 and
                        0 < new_c < grid_size - 1 and
                        (new_r, new_c) not in visited):
                        walls.append((wall_r, wall_c, new_r, new_c))

        # Place exit
        MazeGenerator._place_exit(grid, grid_size)
        return grid

    @staticmethod
    def _generate_backtracking(size):
        """
        Generate maze using recursive backtracking (DFS).
        Creates mazes with long corridors.
        """
        grid_size = 2 * size + 1
        grid = [['#' for _ in range(grid_size)] for _ in range(grid_size)]

        start_row, start_col = 1, 1
        grid[start_row][start_col] = 'S'

        stack = [(start_row, start_col)]
        visited = set()
        visited.add((start_row, start_col))

        directions = [(-2, 0), (0, 2), (2, 0), (0, -2)]

        while stack:
            current_row, current_col = stack[-1]

            neighbors = []
            for dr, dc in directions:
                new_row, new_col = current_row + dr, current_col + dc
                if (0 < new_row < grid_size - 1 and
                    0 < new_col < grid_size - 1 and
                    (new_row, new_col) not in visited):
                    neighbors.append((new_row, new_col, dr, dc))

            if neighbors:
                new_row, new_col, dr, dc = random.choice(neighbors)

                wall_row = current_row + dr // 2
                wall_col = current_col + dc // 2
                grid[wall_row][wall_col] = '.'
                grid[new_row][new_col] = '.'

                visited.add((new_row, new_col))
                stack.append((new_row, new_col))
            else:
                stack.pop()

        MazeGenerator._place_exit(grid, grid_size)
        return grid

    @staticmethod
    def _place_exit(grid, grid_size):
        """Place exit at bottom-right area with opening."""
        exit_placed = False
        for col in range(grid_size - 2, 0, -1):
            for row in range(grid_size - 2, 0, -1):
                if grid[row][col] == '.':
                    grid[row][col] = 'E'
                    if col == grid_size - 2:
                        grid[row][grid_size - 1] = 'E'
                    elif row == grid_size - 2:
                        grid[grid_size - 1][col] = 'E'
                    exit_placed = True
                    break
            if exit_placed:
                break

    @staticmethod
    def generate_rectangular(width=5, height=5, algorithm='prim'):
        """
        Generate a rectangular maze.

        Args:
            width: Width of the maze in cells
            height: Height of the maze in cells
            algorithm: 'prim' (default) or 'backtracking'

        Returns:
            list: 2D grid representing the maze
        """
        grid_width = 2 * width + 1
        grid_height = 2 * height + 1
        grid = [['#' for _ in range(grid_width)] for _ in range(grid_height)]

        start_row, start_col = 1, 1
        grid[start_row][start_col] = 'S'

        directions = [(-2, 0), (0, 2), (2, 0), (0, -2)]

        if algorithm == 'prim':
            # Randomized Prim's algorithm
            walls = []
            visited = set()
            visited.add((start_row, start_col))

            for dr, dc in directions:
                wall_row, wall_col = start_row + dr // 2, start_col + dc // 2
                new_row, new_col = start_row + dr, start_col + dc
                if 0 < new_row < grid_height - 1 and 0 < new_col < grid_width - 1:
                    walls.append((wall_row, wall_col, new_row, new_col))

            while walls:
                wall_row, wall_col, cell_row, cell_col = walls.pop(random.randrange(len(walls)))

                if (cell_row, cell_col) not in visited:
                    grid[wall_row][wall_col] = '.'
                    grid[cell_row][cell_col] = '.'
                    visited.add((cell_row, cell_col))

                    for dr, dc in directions:
                        wall_r, wall_c = cell_row + dr // 2, cell_col + dc // 2
                        new_r, new_c = cell_row + dr, cell_col + dc
                        if (0 < new_r < grid_height - 1 and
                            0 < new_c < grid_width - 1 and
                            (new_r, new_c) not in visited):
                            walls.append((wall_r, wall_c, new_r, new_c))
        else:
            # Recursive backtracking
            stack = [(start_row, start_col)]
            visited = set()
            visited.add((start_row, start_col))

            while stack:
                current_row, current_col = stack[-1]

                neighbors = []
                for dr, dc in directions:
                    new_row, new_col = current_row + dr, current_col + dc
                    if (0 < new_row < grid_height - 1 and
                        0 < new_col < grid_width - 1 and
                        (new_row, new_col) not in visited):
                        neighbors.append((new_row, new_col, dr, dc))

                if neighbors:
                    new_row, new_col, dr, dc = random.choice(neighbors)
                    wall_row = current_row + dr // 2
                    wall_col = current_col + dc // 2
                    grid[wall_row][wall_col] = '.'
                    grid[new_row][new_col] = '.'
                    visited.add((new_row, new_col))
                    stack.append((new_row, new_col))
                else:
                    stack.pop()

        # Place exit
        exit_placed = False
        for col in range(grid_width - 2, 0, -1):
            for row in range(grid_height - 2, 0, -1):
                if grid[row][col] == '.':
                    grid[row][col] = 'E'
                    if col == grid_width - 2:
                        grid[row][grid_width - 1] = 'E'
                    elif row == grid_height - 2:
                        grid[grid_height - 1][col] = 'E'
                    exit_placed = True
                    break
            if exit_placed:
                break

        return grid

    @staticmethod
    def print_maze(grid):
        """
        Print maze to console for debugging.

        Args:
            grid: 2D maze grid
        """
        for row in grid:
            print(''.join(row))
