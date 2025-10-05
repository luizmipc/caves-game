"""
Framework de Labirinto para construir labirintos a partir de layouts de grade.

Símbolos da grade:
- ' ' ou '.' = corredor transitável (cria segmentos de corredor)
- '#' = bloco de parede sólida
- 'S' = posição inicial (transitável)
- 'E' = posição final (transitável)
"""


class MazeFramework:
    """Framework para construir labirintos a partir de layouts de grade ASCII."""

    def __init__(self, grid, cell_size=5.0, wall_height=3.0):
        """
        Inicializa framework de labirinto.

        Args:
            grid: Lista 2D de strings representando o layout do labirinto
            cell_size: Tamanho de cada célula da grade (largura/comprimento)
            wall_height: Altura das paredes e corredores
        """
        self.grid = grid
        self.cell_size = cell_size
        self.wall_height = wall_height
        self.rows = len(grid)
        self.cols = len(grid[0]) if grid else 0

    def get_world_position(self, row, col):
        """
        Converte posição da grade para coordenadas do mundo.

        Args:
            row: Linha da grade
            col: Coluna da grade

        Returns:
            tuple: Posição (x, z) no mundo
        """
        # Centraliza o labirinto na origem
        x = (col - self.cols / 2) * self.cell_size
        z = (row - self.rows / 2) * self.cell_size
        return (x, z)

    def is_walkable(self, cell):
        """Verifica se uma célula é transitável."""
        return cell in ['.', ' ', 'S', 'E']

    def parse(self):
        """
        Analisa a grade e cria paredes/teto para o labirinto.

        Returns:
            dict: Dicionário com posições 'walls', 'ceiling', 'start', 'end'
        """
        from place.wall import Wall
        from place.ceiling import Ceiling

        walls = []
        start_pos = None
        end_pos = None
        ceiling = None

        # Encontra limites do labirinto para o teto
        min_x = min_z = float('inf')
        max_x = max_z = float('-inf')

        # Primeira passagem: encontra limites e marca posições
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
                    # Cria blocos de parede para paredes sólidas
                    wall = Wall(
                        x=x, z=z,
                        width=self.cell_size,
                        height=self.wall_height,
                        depth=self.cell_size
                    )
                    walls.append(wall)

        # Cria um grande teto sobre todas as áreas transitáveis
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
        Adiciona todos os elementos do labirinto a um framework de lugar.

        Args:
            place_framework: Instância de PlaceFramework para adicionar elementos
        """
        elements = self.parse()

        for wall in elements['walls']:
            place_framework.add_element(wall)

        if elements['ceiling']:
            place_framework.add_element(elements['ceiling'])

        return elements['start'], elements['end']
