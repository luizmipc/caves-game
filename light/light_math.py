"""
Light mathematics module.
Handles vector calculations for lighting.
"""

import numpy as np


def calculate_direction_vector(yaw, pitch):
    """
    Calculate direction vector from yaw and pitch angles.

    Args:
        yaw: Horizontal rotation angle in degrees
        pitch: Vertical rotation angle in degrees

    Returns:
        numpy.ndarray: Direction vector [x, y, z]
    """
    yaw_rad = np.radians(yaw)
    pitch_rad = np.radians(pitch)

    dir_x = np.sin(yaw_rad) * np.cos(pitch_rad)
    dir_y = -np.sin(pitch_rad)
    dir_z = -np.cos(yaw_rad) * np.cos(pitch_rad)

    return np.array([dir_x, dir_y, dir_z], dtype=np.float32)


def calculate_light_position(player_pos, direction, distance, height_offset):
    """
    Calculate light position based on player position and direction.

    Args:
        player_pos: Player position [x, y, z]
        direction: Direction vector [x, y, z]
        distance: Distance from player
        height_offset: Vertical offset

    Returns:
        numpy.ndarray: Light position [x, y, z]
    """
    position = player_pos + direction * distance
    position[1] += height_offset
    return position


def check_collision_and_adjust(player_pos, direction, distance, collision_check,
                                min_distance, distance_step, check_radius):
    """
    Check for collisions and adjust distance if needed.

    Args:
        player_pos: Player position [x, y, z]
        direction: Direction vector [x, y, z]
        distance: Initial distance from player
        collision_check: Collision checking function
        min_distance: Minimum allowed distance
        distance_step: Step size for distance reduction
        check_radius: Radius for collision checking

    Returns:
        float: Adjusted distance
    """
    check_distance = distance

    while check_distance > min_distance:
        test_pos = player_pos + direction * check_distance

        if collision_check and collision_check(test_pos[0], test_pos[2], radius=check_radius):
            check_distance -= distance_step
        else:
            break

    return check_distance
