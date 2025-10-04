from .framework import PlaceFramework
from .floor import Floor
from .outside import Outside
from maze.maze import Maze
from maze.generator import MazeGenerator
from player.player_enemy import PlayerEnemy
from spawn.spawn import spawn_at_grid_center
from config import game_config
import random


class Place:
    def __init__(self):
        """Initialize the place/environment using the framework."""
        self.framework = PlaceFramework()

        # Generate and add a random maze using config size
        from maze.maze import Maze
        maze_grid = Maze.generate(size=game_config.maze_size)  # size from config (1-10)
        cell_size = 5.0
        self.cell_size = cell_size

        # Calculate floor size to match maze dimensions exactly
        maze_rows = len(maze_grid)
        maze_cols = len(maze_grid[0]) if maze_grid else 0
        floor_size = max(maze_rows, maze_cols) * cell_size

        # Add outside environment (grass, sky, walls)
        self.outside = Outside(maze_size=floor_size)
        self.framework.add_element(self.outside)

        # Add floor to the place
        floor = Floor(size=floor_size, tile_size=cell_size)
        self.framework.add_element(floor)

        maze = Maze.build(maze_grid, cell_size=cell_size, wall_height=3.0)
        self.start_pos, self.end_pos = maze.add_to_framework(self.framework)

        # Spawn simple ball enemy in a random dead end
        self.player_enemy = None
        dead_ends = MazeGenerator.find_dead_ends(maze_grid)
        if dead_ends:
            # Filter out dead ends that are too close to start or exit
            safe_dead_ends = []
            for row, col in dead_ends:
                # Check distance from start
                if maze_grid[row][col] not in ['S', 'E']:
                    safe_dead_ends.append((row, col))

            if safe_dead_ends:
                # Pick random safe dead end
                dead_end_row, dead_end_col = random.choice(safe_dead_ends)

                # Use shared spawn method (same coordinate system as player spawn)
                enemy_x, enemy_y, enemy_z = spawn_at_grid_center(
                    dead_end_row,
                    dead_end_col,
                    maze_rows,
                    maze_cols,
                    cell_size,
                    y_height=1.5  # Floating height (between floor and eye level)
                )

                self.player_enemy = PlayerEnemy(x=enemy_x, y=enemy_y, z=enemy_z)

                print(f"Enemy ball spawned at ({enemy_x:.2f}, {enemy_y:.2f}, {enemy_z:.2f}) in dead end grid ({dead_end_row}, {dead_end_col})")
                print(f"Maze grid at spawn: '{maze_grid[dead_end_row][dead_end_col]}'")

                # Debug: Check surrounding cells to confirm it's a dead end
                print(f"Surrounding cells: N='{maze_grid[dead_end_row-1][dead_end_col]}' S='{maze_grid[dead_end_row+1][dead_end_col]}' W='{maze_grid[dead_end_row][dead_end_col-1]}' E='{maze_grid[dead_end_row][dead_end_col+1]}'")

    def update(self, delta_time, player_x, player_z):
        """
        Update place elements including enemy AI.

        Returns:
            bool: True if player was caught by enemy, False otherwise
        """
        if self.player_enemy:
            return self.player_enemy.update(delta_time, player_x, player_z, self.framework.check_collision)
        return False

    def render(self):
        """Render all elements of the place."""
        self.framework.render()

    def render_enemy(self, player_x, player_z):
        """Render the enemy billboard facing the player."""
        if self.player_enemy:
            self.player_enemy.render(player_x, player_z)
