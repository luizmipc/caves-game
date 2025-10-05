import pygame


class Camera:
    def __init__(self, sensitivity=0.1):
        """
        Inicializa a câmera com ângulos de rotação.

        Args:
            sensitivity: Sensibilidade do mouse para rotação da câmera
        """
        self.yaw = 0.0  # Rotação horizontal (esquerda/direita)
        self.pitch = 0.0  # Rotação vertical (cima/baixo)
        self.sensitivity = sensitivity

    def handle_mouse_motion(self, dx, dy):
        """
        Lida com o movimento do mouse para rotação da câmera.

        Args:
            dx: Movimento do mouse na direção x
            dy: Movimento do mouse na direção y
        """
        self.yaw += dx * self.sensitivity
        self.pitch += dy * self.sensitivity

        # Limita o pitch para evitar que a câmera vire de cabeça para baixo
        self.pitch = max(-89.0, min(89.0, self.pitch))

    def get_rotation(self):
        """
        Obtém os ângulos de rotação para aplicar à matriz de visualização do OpenGL.

        Returns:
            tuple: (pitch, yaw) em graus
        """
        return (self.pitch, self.yaw)

    def get_yaw(self):
        """Obtém o ângulo yaw atual em graus."""
        return self.yaw

    def get_pitch(self):
        """Obtém o ângulo pitch atual em graus."""
        return self.pitch
