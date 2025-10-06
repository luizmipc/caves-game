import random


class MazeGenerator:
    """Gera labirintos usando vários algoritmos."""

    @staticmethod
    def find_dead_ends(grid):
        """
        Encontra todos os becos sem saída no labirinto (células com apenas uma saída).

        Args:
            grid: Grade 2D do labirinto

        Returns:
            list: Lista de tuplas (linha, coluna) representando posições de becos sem saída
        """
        dead_ends = []
        rows = len(grid)
        cols = len(grid[0]) if rows > 0 else 0

        for row in range(1, rows - 1):
            for col in range(1, cols - 1):
                if grid[row][col] in ['.', 'S', 'E']:
                    # Conta vizinhos abertos
                    open_neighbors = 0
                    if grid[row - 1][col] in ['.', 'S', 'E']:
                        open_neighbors += 1
                    if grid[row + 1][col] in ['.', 'S', 'E']:
                        open_neighbors += 1
                    if grid[row][col - 1] in ['.', 'S', 'E']:
                        open_neighbors += 1
                    if grid[row][col + 1] in ['.', 'S', 'E']:
                        open_neighbors += 1

                    # Beco sem saída tem exatamente 1 vizinho
                    if open_neighbors == 1 and grid[row][col] not in ['S', 'E']:
                        dead_ends.append((row, col))

        return dead_ends

    @staticmethod
    def generate(size=5, algorithm='prim'):
        """
        Gera um labirinto quadrado usando o algoritmo especificado.

        Args:
            size: Tamanho do labirinto (criará uma grade (2*size+1) x (2*size+1))
            algorithm: 'prim' (padrão) ou 'backtracking'

        Returns:
            list: Grade 2D representando o labirinto com paredes '#' e caminhos '.'
        """
        if algorithm == 'prim':
            return MazeGenerator._generate_prim(size)
        else:
            return MazeGenerator._generate_backtracking(size)

    @staticmethod
    def _generate_prim(size):
        """
        Gera labirinto usando o algoritmo de Prim Aleatorizado.
        Cria labirintos com melhor ramificação e caminhos menos previsíveis.
        """
        grid_size = 2 * size + 1
        grid = [['#' for _ in range(grid_size)] for _ in range(grid_size)]

        # Começa de posição aleatória
        start_row, start_col = 1, 1
        grid[start_row][start_col] = 'S'

        # Lista de paredes - paredes adjacentes a células visitadas
        walls = []
        visited = set()
        visited.add((start_row, start_col))

        # Adiciona paredes iniciais
        directions = [(-2, 0), (0, 2), (2, 0), (0, -2)]
        for dr, dc in directions:
            wall_row, wall_col = start_row + dr // 2, start_col + dc // 2
            new_row, new_col = start_row + dr, start_col + dc
            if 0 < new_row < grid_size - 1 and 0 < new_col < grid_size - 1:
                walls.append((wall_row, wall_col, new_row, new_col))

        while walls:
            # Escolhe parede aleatória
            wall_row, wall_col, cell_row, cell_col = walls.pop(random.randrange(len(walls)))

            # Se a célula do outro lado não foi visitada
            if (cell_row, cell_col) not in visited:
                # Torna a parede uma passagem e marca a célula como visitada
                grid[wall_row][wall_col] = '.'
                grid[cell_row][cell_col] = '.'
                visited.add((cell_row, cell_col))

                # Adiciona paredes vizinhas da célula
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
        Gera labirinto usando backtracking recursivo (DFS).
        Cria labirintos com corredores longos.
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
        """Coloca saída na área inferior direita com abertura."""
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
