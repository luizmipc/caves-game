"""
Módulo de luz para o jogo.
Cria uma fonte de luz de bola brilhante que flutua na frente do jogador.
"""

import numpy as np
from .lighting_config import LightingConfig
from .light_math import calculate_direction_vector, calculate_light_position, check_collision_and_adjust
from .light_setup import LightingSetup
from .light_renderer import LightRenderer


class LightBall:
    """Uma bola de luz brilhante que serve como fonte de luz do jogador."""

    def __init__(self, distance=None, height_offset=None, radius=None, light_range=None):
        """
        Inicializa a bola de luz.

        Args:
            distance: Distância na frente do jogador (opcional, usa padrão da config)
            height_offset: Deslocamento de altura relativo ao nível dos olhos do jogador (opcional)
            radius: Raio visual da bola brilhante (opcional)
            light_range: Alcance máximo da iluminação (opcional)
        """
        self.config = LightingConfig()

        # Sobrescreve config com valores fornecidos
        self.distance = distance if distance is not None else self.config.DISTANCE_FROM_PLAYER
        self.height_offset = height_offset if height_offset is not None else self.config.HEIGHT_OFFSET
        self.radius = radius if radius is not None else self.config.BALL_RADIUS
        self.light_range = light_range if light_range is not None else self.config.LIGHT_RANGE

        self.position = np.zeros(3, dtype=np.float32)

    def calculate_position(self, player_x, player_y, player_z, yaw, pitch, collision_check=None):
        """
        Calcula a posição da bola de luz baseada na direção de visão do jogador.

        Args:
            player_x: Posição X do jogador
            player_y: Posição Y do jogador
            player_z: Posição Z do jogador
            yaw: Ângulo yaw do jogador
            pitch: Ângulo pitch do jogador
            collision_check: Função opcional de verificação de colisão
        """
        # Vetor de posição do jogador
        player_pos = np.array([player_x, player_y, player_z], dtype=np.float32)

        # Calcula vetor de direção
        direction = calculate_direction_vector(yaw, pitch)

        # Ajusta distância se colisão detectada
        adjusted_distance = self.distance
        if collision_check:
            adjusted_distance = check_collision_and_adjust(
                player_pos, direction, self.distance, collision_check,
                self.config.MIN_DISTANCE_FROM_WALL,
                self.config.DISTANCE_STEP,
                self.config.COLLISION_CHECK_RADIUS
            )

        # Calcula posição da luz
        self.position = calculate_light_position(
            player_pos, direction, adjusted_distance, self.height_offset
        )

    def setup_lighting(self, player_x, player_y, player_z, yaw, pitch):
        """
        Configura iluminação OpenGL a partir da posição da bola de luz.

        Args:
            player_x: Posição X do jogador
            player_y: Posição Y do jogador
            player_z: Posição Z do jogador
            yaw: Ângulo yaw do jogador
            pitch: Ângulo pitch do jogador
        """
        # Configura parâmetros globais de iluminação
        LightingSetup.setup_global_lighting(self.config.GLOBAL_AMBIENT)

        # Configura neblina para percepção de profundidade
        if self.config.FOG_ENABLED:
            LightingSetup.setup_fog(
                self.config.FOG_COLOR,
                self.config.FOG_START,
                self.config.FOG_END,
                self.config.FOG_DENSITY
            )

        # Calcula direção do spotlight (com deslocamento de pitch)
        adjusted_pitch = pitch + self.config.PITCH_ANGLE_OFFSET
        direction = calculate_direction_vector(yaw, adjusted_pitch)

        # Calcula valores de atenuação
        linear_atten = self.config.LINEAR_ATTENUATION_FACTOR / self.light_range
        quadratic_atten = self.config.QUADRATIC_ATTENUATION_FACTOR / (self.light_range * self.light_range)

        # Configura spotlight
        LightingSetup.setup_spotlight(
            self.position, direction,
            self.config.SPOT_CUTOFF_ANGLE,
            self.config.SPOT_EXPONENT,
            self.config.DIFFUSE_COLOR,
            self.config.AMBIENT_COLOR,
            self.config.SPECULAR_COLOR,
            self.config.CONSTANT_ATTENUATION,
            linear_atten,
            quadratic_atten
        )

        # Configura propriedades do material
        LightingSetup.setup_material_properties(
            self.config.MATERIAL_AMBIENT,
            self.config.MATERIAL_DIFFUSE,
            self.config.MATERIAL_SPECULAR,
            self.config.MATERIAL_SHININESS
        )

    def render_ball(self):
        """Renderiza a própria bola de luz brilhante."""
        LightRenderer.render_glowing_ball(
            self.position,
            self.radius,
            self.config.GLOW_CORE_COLOR,
            self.config.GLOW_OUTER_COLOR,
            self.config.GLOW_OUTER_SIZE_MULTIPLIER
        )

    def disable_lighting(self):
        """Desabilita o sistema de iluminação."""
        LightingSetup.disable_lighting()

    def update_and_render(self, player_x, player_y, player_z, yaw, pitch, collision_check=None):
        """
        Atualiza posição da luz e configura iluminação em uma única chamada.

        Args:
            player_x: Posição X do jogador
            player_y: Posição Y do jogador
            player_z: Posição Z do jogador
            yaw: Ângulo yaw do jogador
            pitch: Ângulo pitch do jogador
            collision_check: Função opcional de verificação de colisão
        """
        # Calcula onde a bola de luz deve estar
        self.calculate_position(player_x, player_y, player_z, yaw, pitch, collision_check)

        # Configura a iluminação a partir desta posição
        self.setup_lighting(player_x, player_y, player_z, yaw, pitch)

        # Renderiza a bola brilhante visível
        self.render_ball()
