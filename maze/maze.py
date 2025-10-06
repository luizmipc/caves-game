from .framework import MazeFramework
from .generator import MazeGenerator


class Maze:
    """
    Utilitários de geração e construção de labirinto.

    Símbolos da grade:
    - '.' ou ' ' = corredor transitável
    - '#' = bloco de parede sólida
    - 'S' = posição inicial (transitável)
    - 'E' = posição final (transitável)
    """

    @staticmethod
    def generate(size=5, algorithm='prim'):
        """
        Gera um labirinto quadrado aleatório.

        Args:
            size: Parâmetro de tamanho (cria grade (2*size+1) x (2*size+1))
                 size=3 -> 7x7, size=5 -> 11x11, size=10 -> 21x21
            algorithm: 'prim' (padrão, melhor ramificação) ou 'backtracking' (corredores longos)

        Returns:
            list: Grade 2D pronta para MazeFramework
        """
        return MazeGenerator.generate(size, algorithm)

    

    @staticmethod
    def build(grid, cell_size=5.0, wall_height=3.0):
        """
        Constrói um labirinto a partir de um layout de grade.

        Args:
            grid: Lista 2D representando layout do labirinto
            cell_size: Tamanho de cada célula da grade
            wall_height: Altura das paredes

        Returns:
            MazeFramework: Instância do framework pronta para adicionar ao lugar
        """
        return MazeFramework(grid, cell_size, wall_height)

    @staticmethod
    def custom(layout_string):
        """
        Constrói um labirinto a partir de uma string multilinha para visualização mais fácil.

        Args:
            layout_string: String multilinha representando o labirinto

        Returns:
            list: Grade 2D pronta para MazeFramework

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
