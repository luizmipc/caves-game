"""Utilitários de spawn para posicionar entidades no labirinto usando o mesmo sistema de coordenadas."""


def grid_to_world_position(row, col, grid_rows, grid_cols, cell_size):
    """
    Converte posição da grade para coordenadas do mundo usando o mesmo método que MazeFramework.

    Args:
        row: Linha da grade
        col: Coluna da grade
        grid_rows: Número total de linhas na grade
        grid_cols: Número total de colunas na grade
        cell_size: Tamanho de cada célula da grade

    Returns:
        tuple: Posição no mundo (x, z) no CENTRO da célula
    """
    # Centraliza o labirinto na origem - mesmo que MazeFramework.get_world_position
    x = (col - grid_cols / 2) * cell_size
    z = (row - grid_rows / 2) * cell_size
    return (x, z)


def spawn_at_grid_center(row, col, grid_rows, grid_cols, cell_size, y_height):
    """
    Obtém posição de spawn no centro de uma célula da grade.

    Args:
        row: Linha da grade
        col: Coluna da grade
        grid_rows: Número total de linhas na grade
        grid_cols: Número total de colunas na grade
        cell_size: Tamanho de cada célula da grade
        y_height: Coordenada Y (altura) para spawn

    Returns:
        tuple: Posição no mundo (x, y, z)
    """
    x, z = grid_to_world_position(row, col, grid_rows, grid_cols, cell_size)
    return (x, y_height, z)
