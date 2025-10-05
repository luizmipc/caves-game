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
        """Inicializa o cenário/ambiente usando o framework."""
        self.framework = PlaceFramework()

        # Gera e adiciona um labirinto aleatório usando o tamanho da configuração
        from maze.maze import Maze
        maze_grid = Maze.generate(size=game_config.maze_size)  # tamanho da configuração (1-10)
        cell_size = 5.0
        self.cell_size = cell_size

        # Calcula o tamanho do piso para corresponder exatamente às dimensões do labirinto
        maze_rows = len(maze_grid)
        maze_cols = len(maze_grid[0]) if maze_grid else 0
        floor_size = max(maze_rows, maze_cols) * cell_size

        # Adiciona ambiente externo (grama, céu, paredes)
        self.outside = Outside(maze_size=floor_size)
        self.framework.add_element(self.outside)

        # Adiciona o piso ao cenário
        floor = Floor(size=floor_size, tile_size=cell_size)
        self.framework.add_element(floor)

        maze = Maze.build(maze_grid, cell_size=cell_size, wall_height=3.0)
        self.start_pos, self.end_pos = maze.add_to_framework(self.framework)

        # Gera inimigo bola simples em um beco sem saída aleatório
        self.player_enemy = None
        dead_ends = MazeGenerator.find_dead_ends(maze_grid)
        if dead_ends:
            # Filtra becos sem saída que estão muito próximos do início ou saída
            safe_dead_ends = []
            for row, col in dead_ends:
                # Verifica distância do início
                if maze_grid[row][col] not in ['S', 'E']:
                    safe_dead_ends.append((row, col))

            if safe_dead_ends:
                # Escolhe um beco sem saída seguro aleatório
                dead_end_row, dead_end_col = random.choice(safe_dead_ends)

                # Usa método de spawn compartilhado (mesmo sistema de coordenadas que o spawn do jogador)
                enemy_x, enemy_y, enemy_z = spawn_at_grid_center(
                    dead_end_row,
                    dead_end_col,
                    maze_rows,
                    maze_cols,
                    cell_size,
                    y_height=1.5  # Altura flutuante (entre o chão e o nível dos olhos)
                )

                self.player_enemy = PlayerEnemy(x=enemy_x, y=enemy_y, z=enemy_z)

                print(f"Enemy ball spawned at ({enemy_x:.2f}, {enemy_y:.2f}, {enemy_z:.2f}) in dead end grid ({dead_end_row}, {dead_end_col})")
                print(f"Maze grid at spawn: '{maze_grid[dead_end_row][dead_end_col]}'")

                # Debug: Verifica células vizinhas para confirmar que é um beco sem saída
                print(f"Surrounding cells: N='{maze_grid[dead_end_row-1][dead_end_col]}' S='{maze_grid[dead_end_row+1][dead_end_col]}' W='{maze_grid[dead_end_row][dead_end_col-1]}' E='{maze_grid[dead_end_row][dead_end_col+1]}'")

    def update(self, delta_time, player_x, player_z):
        """
        Atualiza elementos do cenário incluindo IA do inimigo.

        Returns:
            bool: True se o jogador foi capturado pelo inimigo, False caso contrário
        """
        if self.player_enemy:
            return self.player_enemy.update(delta_time, player_x, player_z, self.framework.check_collision)
        return False

    def render(self):
        """Renderiza todos os elementos do cenário."""
        self.framework.render()

    def render_enemy(self, player_x, player_z):
        """Renderiza o billboard do inimigo virado para o jogador."""
        if self.player_enemy:
            self.player_enemy.render(player_x, player_z)
