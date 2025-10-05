from .camera import Camera
from .movement import Movement


class Player:
    def __init__(self, x=0.0, y=1.7, z=0.0):
        """
        Inicializa jogador com posição, câmera e movimento.

        Args:
            x, y, z: Posição inicial (y é altura, padrão ao nível dos olhos ~1.7m)
        """
        self.x = x
        self.y = y
        self.z = z

        # Inicializa módulos de câmera e movimento
        self.camera = Camera(sensitivity=0.1)
        self.movement = Movement(speed=5.0)

    def handle_mouse_motion(self, dx, dy):
        """
        Trata movimento do mouse para rotação da câmera.

        Args:
            dx: Movimento do mouse na direção x
            dy: Movimento do mouse na direção y
        """
        self.camera.handle_mouse_motion(dx, dy)

    def handle_key_down(self, key):
        """Trata eventos de pressionar tecla."""
        self.movement.handle_key_down(key)

    def handle_key_up(self, key):
        """Trata eventos de soltar tecla."""
        self.movement.handle_key_up(key)

    def update(self, delta_time, collision_check=None):
        """
        Atualiza posição do jogador baseado no estado de movimento.

        Args:
            delta_time: Tempo decorrido desde o último quadro em segundos
            collision_check: Função opcional(x, z) -> bool para verificar colisões
        """
        position = (self.x, self.y, self.z)
        yaw = self.camera.get_yaw()
        self.x, self.y, self.z = self.movement.update(position, yaw, delta_time, collision_check)

    def get_view_matrix_rotation(self):
        """
        Obtém os ângulos de rotação para aplicar à matriz de visualização OpenGL.

        Returns:
            tuple: (pitch, yaw) em graus
        """
        return self.camera.get_rotation()

    def get_position(self):
        """
        Obtém a posição atual do jogador.

        Returns:
            tuple: posição (x, y, z)
        """
        return (self.x, self.y, self.z)
