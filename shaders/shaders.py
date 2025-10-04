"""
Shader module for lighting effects in the game.
Implements a flashlight/torch effect for dark maze exploration.
"""

from OpenGL.GL import *
from OpenGL.GL import shaders


class LightingShader:
    """Simple lighting shader for flashlight effect."""

    # Vertex shader - passes position and calculates distance
    VERTEX_SHADER = """
    #version 120
    varying vec3 fragPosition;

    void main() {
        fragPosition = gl_Vertex.xyz;
        gl_Position = gl_ModelViewProjectionMatrix * gl_Vertex;
    }
    """

    # Fragment shader - creates flashlight effect
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
        Initialize the lighting shader.

        Args:
            light_radius: Radius of the flashlight effect
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
        """Compile vertex and fragment shaders."""
        vertex_shader = shaders.compileShader(self.VERTEX_SHADER, GL_VERTEX_SHADER)
        fragment_shader = shaders.compileShader(self.FRAGMENT_SHADER, GL_FRAGMENT_SHADER)

        self.shader_program = shaders.compileProgram(vertex_shader, fragment_shader)

        # Get uniform locations
        self.player_pos_location = glGetUniformLocation(self.shader_program, b"playerPosition")
        self.light_radius_location = glGetUniformLocation(self.shader_program, b"lightRadius")
        self.base_color_location = glGetUniformLocation(self.shader_program, b"baseColor")

    def use(self, player_x, player_y, player_z, base_color=(1.0, 1.0, 1.0)):
        """
        Activate the shader with player position.

        Args:
            player_x: Player X position
            player_y: Player Y position
            player_z: Player Z position
            base_color: RGB color tuple for lit surfaces
        """
        if self.shader_program is None:
            return

        shaders.glUseProgram(self.shader_program)

        # Set uniforms
        if self.player_pos_location != -1:
            glUniform3f(self.player_pos_location, player_x, player_y, player_z)

        if self.light_radius_location != -1:
            glUniform1f(self.light_radius_location, self.light_radius)

        if self.base_color_location != -1:
            glUniform3f(self.base_color_location, base_color[0], base_color[1], base_color[2])

    def disable(self):
        """Disable the shader."""
        if self.shader_program is not None:
            shaders.glUseProgram(0)


class SimpleLighting:
    """Simpler OpenGL fixed-function lighting as fallback."""

    def __init__(self, light_radius=10.0):
        """
        Initialize simple lighting.

        Args:
            light_radius: Radius of the light effect
        """
        self.light_radius = light_radius

    def setup(self, player_x, player_y, player_z):
        """
        Setup OpenGL lighting at player position.

        Args:
            player_x: Player X position
            player_y: Player Y position
            player_z: Player Z position
        """
        glEnable(GL_LIGHTING)
        glEnable(GL_LIGHT0)

        # Position light at player
        glLightfv(GL_LIGHT0, GL_POSITION, [player_x, player_y, player_z, 1.0])

        # White light
        glLightfv(GL_LIGHT0, GL_DIFFUSE, [1.0, 1.0, 1.0, 1.0])
        glLightfv(GL_LIGHT0, GL_AMBIENT, [0.1, 0.1, 0.1, 1.0])
        glLightfv(GL_LIGHT0, GL_SPECULAR, [0.5, 0.5, 0.5, 1.0])

        # Attenuation based on radius
        glLightf(GL_LIGHT0, GL_CONSTANT_ATTENUATION, 1.0)
        glLightf(GL_LIGHT0, GL_LINEAR_ATTENUATION, 2.0 / self.light_radius)
        glLightf(GL_LIGHT0, GL_QUADRATIC_ATTENUATION, 1.0 / (self.light_radius * self.light_radius))

        # Enable color material
        glEnable(GL_COLOR_MATERIAL)
        glColorMaterial(GL_FRONT_AND_BACK, GL_AMBIENT_AND_DIFFUSE)

    def disable(self):
        """Disable lighting."""
        glDisable(GL_LIGHTING)
        glDisable(GL_LIGHT0)
        glDisable(GL_COLOR_MATERIAL)
