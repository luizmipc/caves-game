"""
Módulo de shader para efeitos de iluminação no jogo.
Implementa um efeito de lanterna/tocha para exploração de labirinto escuro.
"""

from OpenGL.GL import *
from OpenGL.GL import shaders


class LightingShader:
    """Shader de iluminação simples para efeito de lanterna."""

    # Vertex shader - passa posição e calcula distância
    VERTEX_SHADER = """
    #version 120
    varying vec3 fragPosition;

    void main() {
        fragPosition = gl_Vertex.xyz;
        gl_Position = gl_ModelViewProjectionMatrix * gl_Vertex;
    }
    """

    # Fragment shader - cria efeito de lanterna
    FRAGMENT_SHADER = """
    #version 120
    uniform vec3 playerPosition;
    uniform float lightRadius;
    uniform vec3 baseColor;

    varying vec3 fragPosition;

    void main() {
        float dist = distance(fragPosition, playerPosition);
        float attenuation = 1.0 - smoothstep(0.0, lightRadius, dist);

        vec3 litColor = baseColor * attenuation;
        gl_FragColor = vec4(litColor, 1.0);
    }
    """

    def __init__(self, light_radius=10.0):
        """
        Inicializa o shader de iluminação.

        Args:
            light_radius: Raio do efeito de lanterna
        """
        self.light_radius = light_radius
        self.shader_program = None
        self.player_pos_location = None
        self.light_radius_location = None
        self.base_color_location = None

        try:
            self._compile_shaders()
        except Exception as e:
            print(f"Shader compilation failed: {e}")
            print("Falling back to fixed-function pipeline")

    def _compile_shaders(self):
        """Compila shaders de vértice e fragmento."""
        vertex_shader = shaders.compileShader(self.VERTEX_SHADER, GL_VERTEX_SHADER)
        fragment_shader = shaders.compileShader(self.FRAGMENT_SHADER, GL_FRAGMENT_SHADER)

        self.shader_program = shaders.compileProgram(vertex_shader, fragment_shader)

        # Obtém localizações de uniformes
        self.player_pos_location = glGetUniformLocation(self.shader_program, b"playerPosition")
        self.light_radius_location = glGetUniformLocation(self.shader_program, b"lightRadius")
        self.base_color_location = glGetUniformLocation(self.shader_program, b"baseColor")

    def use(self, player_x, player_y, player_z, base_color=(1.0, 1.0, 1.0)):
        """
        Ativa o shader com a posição do jogador.

        Args:
            player_x: Posição X do jogador
            player_y: Posição Y do jogador
            player_z: Posição Z do jogador
            base_color: Tupla de cor RGB para superfícies iluminadas
        """
        if self.shader_program is None:
            return

        shaders.glUseProgram(self.shader_program)

        # Define uniformes
        if self.player_pos_location != -1:
            glUniform3f(self.player_pos_location, player_x, player_y, player_z)

        if self.light_radius_location != -1:
            glUniform1f(self.light_radius_location, self.light_radius)

        if self.base_color_location != -1:
            glUniform3f(self.base_color_location, base_color[0], base_color[1], base_color[2])

    def disable(self):
        """Desabilita o shader."""
        if self.shader_program is not None:
            shaders.glUseProgram(0)


class SimpleLighting:
    """Iluminação de função fixa do OpenGL mais simples como alternativa."""

    def __init__(self, light_radius=10.0):
        """
        Inicializa iluminação simples.

        Args:
            light_radius: Raio do efeito de luz
        """
        self.light_radius = light_radius

    def setup(self, player_x, player_y, player_z):
        """
        Configura iluminação OpenGL na posição do jogador.

        Args:
            player_x: Posição X do jogador
            player_y: Posição Y do jogador
            player_z: Posição Z do jogador
        """
        glEnable(GL_LIGHTING)
        glEnable(GL_LIGHT0)

        # Posiciona luz no jogador
        glLightfv(GL_LIGHT0, GL_POSITION, [player_x, player_y, player_z, 1.0])

        # Luz branca
        glLightfv(GL_LIGHT0, GL_DIFFUSE, [1.0, 1.0, 1.0, 1.0])
        glLightfv(GL_LIGHT0, GL_AMBIENT, [0.1, 0.1, 0.1, 1.0])
        glLightfv(GL_LIGHT0, GL_SPECULAR, [0.5, 0.5, 0.5, 1.0])

        # Atenuação baseada no raio
        glLightf(GL_LIGHT0, GL_CONSTANT_ATTENUATION, 1.0)
        glLightf(GL_LIGHT0, GL_LINEAR_ATTENUATION, 2.0 / self.light_radius)
        glLightf(GL_LIGHT0, GL_QUADRATIC_ATTENUATION, 1.0 / (self.light_radius * self.light_radius))

        # Habilita material colorido
        glEnable(GL_COLOR_MATERIAL)
        glColorMaterial(GL_FRONT_AND_BACK, GL_AMBIENT_AND_DIFFUSE)

    def disable(self):
        """Desabilita iluminação."""
        glDisable(GL_LIGHTING)
        glDisable(GL_LIGHT0)
        glDisable(GL_COLOR_MATERIAL)
