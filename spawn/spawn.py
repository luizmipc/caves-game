"""Spawn utilities for placing entities in the maze using the same coordinate system."""


def grid_to_world_position(row, col, grid_rows, grid_cols, cell_size):
    """
    Convert grid position to world coordinates using the same method as MazeFramework.

    Args:
        row: Grid row
        col: Grid column
        grid_rows: Total number of rows in grid
        grid_cols: Total number of columns in grid
        cell_size: Size of each grid cell

    Returns:
        tuple: (x, z) world position at the CENTER of the cell
    """
    # Center the maze at origin - same as MazeFramework.get_world_position
    x = (col - grid_cols / 2) * cell_size
    z = (row - grid_rows / 2) * cell_size
    return (x, z)


def spawn_at_grid_center(row, col, grid_rows, grid_cols, cell_size, y_height):
    """
    Get spawn position at the center of a grid cell.

    Args:
        row: Grid row
        col: Grid column
        grid_rows: Total number of rows in grid
        grid_cols: Total number of columns in grid
        cell_size: Size of each grid cell
        y_height: Y coordinate (height) for spawn

    Returns:
        tuple: (x, y, z) world position
    """
    x, z = grid_to_world_position(row, col, grid_rows, grid_cols, cell_size)
    return (x, y_height, z)
