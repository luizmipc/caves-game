"""
Advanced lighting simulation module.
Implements multi-bounce lighting and surface reflections for realistic illumination.
"""

from OpenGL.GL import *
from OpenGL.GL import shaders
import numpy as np


class AdvancedLighting:
    """Advanced lighting with indirect illumination and reflections."""

    # Vertex shader with additional outputs
    VERTEX_SHADER = """
    #version 120
    varying vec3 fragPosition;
    varying vec3 fragNormal;
    varying vec3 viewSpacePos;

    void main() {
        // Transform vertex to view space
        vec4 viewPos = gl_ModelViewMatrix * gl_Vertex;
        viewSpacePos = viewPos.xyz;
        fragPosition = vec3(gl_ModelViewMatrix * gl_Vertex);
        fragNormal = normalize(gl_NormalMatrix * gl_Normal);

        gl_Position = gl_ModelViewProjectionMatrix * gl_Vertex;
        gl_FrontColor = gl_Color;
        gl_TexCoord[0] = gl_MultiTexCoord0;
    }
    """

    # Fragment shader with advanced lighting
    FRAGMENT_SHADER = """
    #version 120
    uniform vec3 lightPosition;
    uniform vec3 lightDirection;
    uniform float spotCutoff;
    uniform float spotExponent;

    uniform vec3 diffuseColor;
    uniform vec3 ambientColor;
    uniform vec3 specularColor;

    uniform float constantAtten;
    uniform float linearAtten;
    uniform float quadraticAtten;

    uniform vec3 globalAmbient;
    uniform float reflectivity;  // Surface reflectivity for indirect light
    uniform float indirectStrength;  // Strength of indirect lighting

    varying vec3 fragPosition;
    varying vec3 fragNormal;
    varying vec3 viewSpacePos;

    // Approximate indirect lighting from nearby surfaces
    vec3 calculateIndirectLight(vec3 normal, vec3 surfaceColor) {
        // Simple hemisphere sampling for indirect light
        vec3 indirect = vec3(0.0);

        // Sample light bouncing from floor (below)
        vec3 floorDir = vec3(0.0, -1.0, 0.0);
        float floorContribution = max(0.0, dot(normal, -floorDir)) * 0.3;
        indirect += surfaceColor * floorContribution * indirectStrength;

        // Sample light bouncing from ceiling (above)
        vec3 ceilingDir = vec3(0.0, 1.0, 0.0);
        float ceilingContribution = max(0.0, dot(normal, -ceilingDir)) * 0.2;
        indirect += surfaceColor * ceilingContribution * indirectStrength;

        // Sample light bouncing from walls (sides)
        vec3 wallDirs[4];
        wallDirs[0] = vec3(1.0, 0.0, 0.0);
        wallDirs[1] = vec3(-1.0, 0.0, 0.0);
        wallDirs[2] = vec3(0.0, 0.0, 1.0);
        wallDirs[3] = vec3(0.0, 0.0, -1.0);

        for (int i = 0; i < 4; i++) {
            float wallContribution = max(0.0, dot(normal, -wallDirs[i])) * 0.15;
            indirect += surfaceColor * wallContribution * indirectStrength;
        }

        return indirect;
    }

    void main() {
        vec3 normal = normalize(fragNormal);
        vec3 lightDir = normalize(lightPosition - fragPosition);
        vec3 viewDir = normalize(-viewSpacePos);

        // Distance attenuation
        float distance = length(lightPosition - fragPosition);
        float attenuation = 1.0 / (constantAtten + linearAtten * distance + quadraticAtten * distance * distance);

        // Spotlight calculation
        vec3 spotDir = normalize(lightDirection);
        float spotEffect = 0.0;
        float spotDot = dot(-lightDir, spotDir);
        float spotAngle = acos(spotDot) * 180.0 / 3.14159;

        if (spotAngle < spotCutoff) {
            float intensity = 1.0 - (spotAngle / spotCutoff);
            spotEffect = pow(intensity, spotExponent);
        }

        // Diffuse lighting
        float diffuseFactor = max(dot(normal, lightDir), 0.0);
        vec3 diffuse = diffuseColor * gl_Color.rgb * diffuseFactor * attenuation * spotEffect;

        // Specular lighting (Blinn-Phong)
        vec3 halfDir = normalize(lightDir + viewDir);
        float specFactor = pow(max(dot(normal, halfDir), 0.0), 32.0);
        vec3 specular = specularColor * specFactor * attenuation * spotEffect;

        // Ambient lighting
        vec3 ambient = globalAmbient * gl_Color.rgb + ambientColor * gl_Color.rgb * attenuation;

        // Indirect lighting (bounced light from surfaces)
        vec3 indirect = calculateIndirectLight(normal, gl_Color.rgb);

        // Surface reflectivity affects how much light bounces
        indirect *= reflectivity * spotEffect * attenuation;

        // Combine all lighting components
        vec3 finalColor = ambient + diffuse + specular + indirect;

        // Add slight distance fog for depth perception
        float fogFactor = exp(-distance * 0.05);
        finalColor = mix(vec3(0.0), finalColor, fogFactor);

        gl_FragColor = vec4(finalColor, gl_Color.a);
    }
    """

    def __init__(self):
        """Initialize advanced lighting shader."""
        self.shader_program = None
        self.uniform_locations = {}

        try:
            self._compile_shaders()
        except Exception as e:
            print(f"Advanced lighting shader compilation failed: {e}")
            self.shader_program = None

    def _compile_shaders(self):
        """Compile vertex and fragment shaders."""
        vertex_shader = shaders.compileShader(self.VERTEX_SHADER, GL_VERTEX_SHADER)
        fragment_shader = shaders.compileShader(self.FRAGMENT_SHADER, GL_FRAGMENT_SHADER)

        self.shader_program = shaders.compileProgram(vertex_shader, fragment_shader)

        # Get uniform locations
        uniforms = [
            'lightPosition', 'lightDirection', 'spotCutoff', 'spotExponent',
            'diffuseColor', 'ambientColor', 'specularColor',
            'constantAtten', 'linearAtten', 'quadraticAtten',
            'globalAmbient', 'reflectivity', 'indirectStrength'
        ]

        for uniform in uniforms:
            self.uniform_locations[uniform] = glGetUniformLocation(
                self.shader_program, uniform.encode()
            )

    def use(self, light_pos, light_dir, config):
        """
        Activate advanced lighting shader.

        Args:
            light_pos: Light position [x, y, z]
            light_dir: Light direction [x, y, z]
            config: LightingConfig instance

        Returns:
            bool: True if shader is active, False otherwise
        """
        if self.shader_program is None:
            return False

        shaders.glUseProgram(self.shader_program)

        # Set light properties
        glUniform3f(self.uniform_locations['lightPosition'],
                   light_pos[0], light_pos[1], light_pos[2])
        glUniform3f(self.uniform_locations['lightDirection'],
                   light_dir[0], light_dir[1], light_dir[2])
        glUniform1f(self.uniform_locations['spotCutoff'], config.SPOT_CUTOFF_ANGLE)
        glUniform1f(self.uniform_locations['spotExponent'], config.SPOT_EXPONENT)

        # Set light colors
        glUniform3f(self.uniform_locations['diffuseColor'],
                   config.DIFFUSE_COLOR[0], config.DIFFUSE_COLOR[1], config.DIFFUSE_COLOR[2])
        glUniform3f(self.uniform_locations['ambientColor'],
                   config.AMBIENT_COLOR[0], config.AMBIENT_COLOR[1], config.AMBIENT_COLOR[2])
        glUniform3f(self.uniform_locations['specularColor'],
                   config.SPECULAR_COLOR[0], config.SPECULAR_COLOR[1], config.SPECULAR_COLOR[2])

        # Set attenuation
        linear_atten = config.LINEAR_ATTENUATION_FACTOR / config.LIGHT_RANGE
        quadratic_atten = config.QUADRATIC_ATTENUATION_FACTOR / (config.LIGHT_RANGE ** 2)

        glUniform1f(self.uniform_locations['constantAtten'], config.CONSTANT_ATTENUATION)
        glUniform1f(self.uniform_locations['linearAtten'], linear_atten)
        glUniform1f(self.uniform_locations['quadraticAtten'], quadratic_atten)

        # Set global lighting
        glUniform3f(self.uniform_locations['globalAmbient'],
                   config.GLOBAL_AMBIENT[0], config.GLOBAL_AMBIENT[1], config.GLOBAL_AMBIENT[2])

        # Set indirect lighting properties
        glUniform1f(self.uniform_locations['reflectivity'], 0.3)  # Surfaces reflect 30% of light
        glUniform1f(self.uniform_locations['indirectStrength'], 0.4)  # Indirect light strength

        return True

    def disable(self):
        """Disable the shader."""
        if self.shader_program is not None:
            shaders.glUseProgram(0)
