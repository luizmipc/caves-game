"""
Módulo de matemática de luz.
Lida com cálculos vetoriais para iluminação.
"""

import numpy as np


def calculate_direction_vector(yaw, pitch):
    """
    Calcula vetor de direção a partir dos ângulos yaw e pitch.

    Args:
        yaw: Ângulo de rotação horizontal em graus
        pitch: Ângulo de rotação vertical em graus

    Returns:
        numpy.ndarray: Vetor de direção [x, y, z]
    """
    yaw_rad = np.radians(yaw)
    pitch_rad = np.radians(pitch)

    dir_x = np.sin(yaw_rad) * np.cos(pitch_rad)
    dir_y = -np.sin(pitch_rad)
    dir_z = -np.cos(yaw_rad) * np.cos(pitch_rad)

    return np.array([dir_x, dir_y, dir_z], dtype=np.float32)


def calculate_light_position(player_pos, direction, distance, height_offset):
    """
    Calcula posição da luz baseada na posição e direção do jogador.

    Args:
        player_pos: Posição do jogador [x, y, z]
        direction: Vetor de direção [x, y, z]
        distance: Distância do jogador
        height_offset: Deslocamento vertical

    Returns:
        numpy.ndarray: Posição da luz [x, y, z]
    """
    position = player_pos + direction * distance
    position[1] += height_offset
    return position


def check_collision_and_adjust(player_pos, direction, distance, collision_check,
                                min_distance, distance_step, check_radius):
    """
    Verifica colisões e ajusta distância se necessário.

    Args:
        player_pos: Posição do jogador [x, y, z]
        direction: Vetor de direção [x, y, z]
        distance: Distância inicial do jogador
        collision_check: Função de verificação de colisão
        min_distance: Distância mínima permitida
        distance_step: Tamanho do passo para redução de distância
        check_radius: Raio para verificação de colisão

    Returns:
        float: Distância ajustada
    """
    check_distance = distance

    while check_distance > min_distance:
        test_pos = player_pos + direction * check_distance

        if collision_check and collision_check(test_pos[0], test_pos[2], radius=check_radius):
            check_distance -= distance_step
        else:
            break

    return check_distance
