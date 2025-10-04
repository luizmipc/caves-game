"""
Elliptical spotlight shader module.
Creates a spotlight with different horizontal and vertical cone angles.
"""

from OpenGL.GL import *
from OpenGL.GL import shaders
import numpy as np


class EllipticalSpotlight:
    """Custom shader-based elliptical spotlight."""

    # Vertex shader - standard pass-through with position
    VERTEX_SHADER = """
    #version 120
    varying vec3 fragPosition;
    varying vec3 fragNormal;

    void main() {
        fragPosition = vec3(gl_ModelViewMatrix * gl_Vertex);
        fragNormal = normalize(gl_NormalMatrix * gl_Normal);
        gl_Position = gl_ModelViewProjectionMatrix * gl_Vertex;
        gl_FrontColor = gl_Color;
    }
    """

    # Fragment shader - elliptical spotlight calculation
    FRAGMENT_SHADER = """
    #version 120
    uniform vec3 lightPosition;
    uniform vec3 lightDirection;
    uniform float horizontalAngle;  // In radians
    uniform float verticalAngle;    // In radians
    uniform vec3 diffuseColor;
    uniform vec3 ambientColor;
    uniform vec3 specularColor;
    uniform float constantAtten;
    uniform float linearAtten;
    uniform float quadraticAtten;
    uniform float spotExponent;
    uniform vec3 globalAmbient;

    varying vec3 fragPosition;
    varying vec3 fragNormal;

    void main() {
        // Direction from fragment to light
        vec3 lightDir = normalize(lightPosition - fragPosition);

        // Distance attenuation
        float distance = length(lightPosition - fragPosition);
        float attenuation = 1.0 / (constantAtten + linearAtten * distance + quadraticAtten * distance * distance);

        // Calculate angle between light direction and fragment direction
        vec3 spotDir = normalize(lightDirection);
        float cosAngle = dot(-lightDir, spotDir);

        // Transform to spotlight's coordinate system to check elliptical cone
        vec3 up = vec3(0.0, 1.0, 0.0);
        vec3 right = normalize(cross(spotDir, up));
        vec3 actualUp = cross(right, spotDir);

        // Project light-to-fragment direction onto spotlight's coordinate system
        vec3 fragDir = -lightDir;
        float horizontalComponent = dot(fragDir, right);
        float verticalComponent = dot(fragDir, actualUp);
        float forwardComponent = dot(fragDir, spotDir);

        // Calculate angles in each direction
        float horizAngle = atan(horizontalComponent, forwardComponent);
        float vertAngle = atan(verticalComponent, forwardComponent);

        // Check if within elliptical cone
        float horizFactor = horizAngle / horizontalAngle;
        float vertFactor = vertAngle / verticalAngle;
        float ellipticalFactor = horizFactor * horizFactor + vertFactor * vertFactor;

        float spotEffect = 0.0;
        if (ellipticalFactor <= 1.0 && forwardComponent > 0.0) {
            // Inside elliptical cone
            float intensity = 1.0 - sqrt(ellipticalFactor);
            spotEffect = pow(intensity, spotExponent);
        }

        // Lighting calculations
        vec3 normal = normalize(fragNormal);
        float diffuseFactor = max(dot(normal, lightDir), 0.0);

        // Ambient component (global + light ambient)
        vec3 ambient = globalAmbient * gl_Color.rgb + ambientColor * gl_Color.rgb * attenuation;

        // Diffuse component
        vec3 diffuse = diffuseColor * gl_Color.rgb * diffuseFactor * attenuation * spotEffect;

        // Specular component
        vec3 viewDir = normalize(-fragPosition);
        vec3 reflectDir = reflect(-lightDir, normal);
        float specFactor = pow(max(dot(viewDir, reflectDir), 0.0), 20.0);
        vec3 specular = specularColor * specFactor * attenuation * spotEffect;

        // Final color
        vec3 finalColor = ambient + diffuse + specular;
        gl_FragColor = vec4(finalColor, gl_Color.a);
    }
    """

    def __init__(self, horizontal_angle=20.0, vertical_angle=35.0):
        """
        Initialize elliptical spotlight shader.

        Args:
            horizontal_angle: Horizontal cone angle in degrees
            vertical_angle: Vertical cone angle in degrees
        """
        self.horizontal_angle_deg = horizontal_angle
        self.vertical_angle_deg = vertical_angle
        self.horizontal_angle_rad = np.radians(horizontal_angle)
        self.vertical_angle_rad = np.radians(vertical_angle)

        self.shader_program = None
        self.uniform_locations = {}

        try:
            self._compile_shaders()
        except Exception as e:
            print(f"Elliptical spotlight shader compilation failed: {e}")
            self.shader_program = None

    def _compile_shaders(self):
        """Compile vertex and fragment shaders."""
        vertex_shader = shaders.compileShader(self.VERTEX_SHADER, GL_VERTEX_SHADER)
        fragment_shader = shaders.compileShader(self.FRAGMENT_SHADER, GL_FRAGMENT_SHADER)

        self.shader_program = shaders.compileProgram(vertex_shader, fragment_shader)

        # Get uniform locations
        uniforms = [
            'lightPosition', 'lightDirection', 'horizontalAngle', 'verticalAngle',
            'diffuseColor', 'ambientColor', 'specularColor',
            'constantAtten', 'linearAtten', 'quadraticAtten',
            'spotExponent', 'globalAmbient'
        ]

        for uniform in uniforms:
            self.uniform_locations[uniform] = glGetUniformLocation(
                self.shader_program, uniform.encode()
            )

    def use(self, light_pos, light_dir, config):
        """
        Activate the shader with parameters.

        Args:
            light_pos: Light position [x, y, z]
            light_dir: Light direction [x, y, z]
            config: LightingConfig instance
        """
        if self.shader_program is None:
            return False

        shaders.glUseProgram(self.shader_program)

        # Set uniforms
        glUniform3f(self.uniform_locations['lightPosition'],
                   light_pos[0], light_pos[1], light_pos[2])
        glUniform3f(self.uniform_locations['lightDirection'],
                   light_dir[0], light_dir[1], light_dir[2])
        glUniform1f(self.uniform_locations['horizontalAngle'], self.horizontal_angle_rad)
        glUniform1f(self.uniform_locations['verticalAngle'], self.vertical_angle_rad)

        glUniform3f(self.uniform_locations['diffuseColor'],
                   config.DIFFUSE_COLOR[0], config.DIFFUSE_COLOR[1], config.DIFFUSE_COLOR[2])
        glUniform3f(self.uniform_locations['ambientColor'],
                   config.AMBIENT_COLOR[0], config.AMBIENT_COLOR[1], config.AMBIENT_COLOR[2])
        glUniform3f(self.uniform_locations['specularColor'],
                   config.SPECULAR_COLOR[0], config.SPECULAR_COLOR[1], config.SPECULAR_COLOR[2])

        linear_atten = config.LINEAR_ATTENUATION_FACTOR / config.LIGHT_RANGE
        quadratic_atten = config.QUADRATIC_ATTENUATION_FACTOR / (config.LIGHT_RANGE ** 2)

        glUniform1f(self.uniform_locations['constantAtten'], config.CONSTANT_ATTENUATION)
        glUniform1f(self.uniform_locations['linearAtten'], linear_atten)
        glUniform1f(self.uniform_locations['quadraticAtten'], quadratic_atten)
        glUniform1f(self.uniform_locations['spotExponent'], config.SPOT_EXPONENT)

        glUniform3f(self.uniform_locations['globalAmbient'],
                   config.GLOBAL_AMBIENT[0], config.GLOBAL_AMBIENT[1], config.GLOBAL_AMBIENT[2])

        return True

    def disable(self):
        """Disable the shader."""
        if self.shader_program is not None:
            shaders.glUseProgram(0)
