import numpy as np
import pygame


class Movement:
    def __init__(self, speed=5.0):
        """
        Inicializa o controlador de movimento.

        Args:
            speed: Velocidade de movimento em unidades por segundo
        """
        self.speed = speed

        # Estado de movimento
        self.moving_forward = False
        self.moving_backward = False
        self.moving_left = False
        self.moving_right = False

    def handle_key_down(self, key):
        """Lida com eventos de pressionamento de tecla."""
        if key == pygame.K_w:
            self.moving_forward = True
        elif key == pygame.K_s:
            self.moving_backward = True
        elif key == pygame.K_a:
            self.moving_left = True
        elif key == pygame.K_d:
            self.moving_right = True

    def handle_key_up(self, key):
        """Lida com eventos de liberação de tecla."""
        if key == pygame.K_w:
            self.moving_forward = False
        elif key == pygame.K_s:
            self.moving_backward = False
        elif key == pygame.K_a:
            self.moving_left = False
        elif key == pygame.K_d:
            self.moving_right = False

    def update(self, position, yaw, delta_time, collision_check=None):
        """
        Calcula nova posição com base no estado de movimento e yaw da câmera.

        Args:
            position: Tupla de posição atual (x, y, z)
            yaw: Ângulo yaw da câmera em graus
            delta_time: Tempo decorrido desde o último frame em segundos
            collision_check: Função opcional(x, z) -> bool para verificar colisões

        Returns:
            tuple: Nova posição (x, y, z)
        """
        x, y, z = position
        yaw_rad = np.radians(yaw)
        new_x, new_z = x, z

        # Movimento para frente/trás
        if self.moving_forward:
            new_x += np.sin(yaw_rad) * self.speed * delta_time
            new_z -= np.cos(yaw_rad) * self.speed * delta_time
        if self.moving_backward:
            new_x -= np.sin(yaw_rad) * self.speed * delta_time
            new_z += np.cos(yaw_rad) * self.speed * delta_time

        # Movimento lateral esquerda/direita
        if self.moving_left:
            new_x -= np.cos(yaw_rad) * self.speed * delta_time
            new_z -= np.sin(yaw_rad) * self.speed * delta_time
        if self.moving_right:
            new_x += np.cos(yaw_rad) * self.speed * delta_time
            new_z += np.sin(yaw_rad) * self.speed * delta_time

        # Verifica colisão antes de aplicar movimento
        if collision_check is None or not collision_check(new_x, new_z):
            x, z = new_x, new_z

        return (x, y, z)
