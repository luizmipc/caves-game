"""
Módulo de configuração de iluminação.

Configuração centralizada para todos os parâmetros de iluminação usados no jogo.
Este módulo define a fonte de luz tipo tocha que cria a atmosfera
estética dreamcore/horror liminal.

O sistema de iluminação usa:
- Temperatura de cor quente (como uma tocha ou lanterna)
- Cone de spotlight para iluminação direcionada
- Atenuação de distância para queda realista
- Neblina para profundidade atmosférica
- Propriedades de material para interação de superfície
"""

import numpy as np


class LightingConfig:
    """
    Configurações para o sistema de iluminação.

    Todos os valores podem ser ajustados para mudar a sensação da luz.
    As configurações atuais criam uma atmosfera quente, tipo tocha com
    queda realista e bordas suaves.
    """

    # ===== PROPRIEDADES FÍSICAS DA BOLA DE LUZ =====
    # Posição da fonte de luz relativa ao jogador
    DISTANCE_FROM_PLAYER = -1.2  # Negativo = atrás do jogador (oculto da visão)
    HEIGHT_OFFSET = -0.3  # Negativo = abaixo do nível dos olhos (evita ver a bola de luz)
    BALL_RADIUS = 0.15  # Tamanho visual do orbe brilhante (se visível)
    LIGHT_RANGE = 15.0  # Distância máxima que a luz alcança

    # ===== PROPRIEDADES DO SPOTLIGHT =====
    # Define o cone de luz
    SPOT_CUTOFF_ANGLE = 35.0  # Ângulo do cone em graus (35° = amplo mas focado)
    SPOT_EXPONENT = 0.5  # Suavidade da borda (menor = mais suave, maior = mais nítida)
    PITCH_ANGLE_OFFSET = 0.0  # Deslocamento de mira vertical (0 = aponta para onde o jogador olha)

    # ===== INTENSIDADE DA LUZ (valores RGB) =====
    # Temperatura de cor quente cria realismo tipo tocha
    # Nota: Valores > 1.0 criam iluminação excessiva (intencional para iluminação forte)
    DIFFUSE_COLOR = np.array([12.0, 11.5, 10.5, 1.0], dtype=np.float32)  # Luz principal (branco/laranja quente)
    AMBIENT_COLOR = np.array([5.0, 4.7, 4.2, 1.0], dtype=np.float32)  # Luz de preenchimento (garante visibilidade)
    SPECULAR_COLOR = np.array([6.5, 5.8, 4.8, 1.0], dtype=np.float32)  # Destaques (superfícies refletivas)

    # Luz ambiente global (leve brilho mesmo na sombra)
    GLOBAL_AMBIENT = np.array([0.2, 0.2, 0.2, 1.0], dtype=np.float32)

    # ===== ATENUAÇÃO (Queda da Luz com Distância) =====
    # Fórmula: atenuação = 1.0 / (constante + linear*distância + quadrática*distância²)
    # Valores menores = luz alcança mais longe
    CONSTANT_ATTENUATION = 0.1  # Atenuação base (brilho na fonte)
    LINEAR_ATTENUATION_FACTOR = 0.4  # Taxa de queda linear
    QUADRATIC_ATTENUATION_FACTOR = 1.2  # Queda quadrática (lei do inverso do quadrado)

    # ===== PROPRIEDADES DO MATERIAL =====
    # Como as superfícies reagem à luz
    MATERIAL_AMBIENT = np.array([0.28, 0.26, 0.23, 1.0], dtype=np.float32)  # Cor base da superfície
    MATERIAL_DIFFUSE = np.array([0.95, 0.95, 0.95, 1.0], dtype=np.float32)  # Absorção de luz (0.95 = muito responsivo)
    MATERIAL_SPECULAR = np.array([0.5, 0.45, 0.35, 1.0], dtype=np.float32)  # Cor do brilho
    MATERIAL_SHININESS = 12.0  # Fator de brilho (menor = destaques mais amplos)

    # ===== PROPRIEDADES DO BRILHO DA BOLA =====
    # Aparência visual da própria bola de luz (se visível)
    GLOW_CORE_COLOR = np.array([1.0, 0.95, 0.75, 1.0], dtype=np.float32)  # Centro (branco quente brilhante)
    GLOW_OUTER_COLOR = np.array([1.0, 0.85, 0.5, 0.4], dtype=np.float32)  # Borda (laranja com transparência)
    GLOW_OUTER_SIZE_MULTIPLIER = 1.6  # Tamanho do brilho externo relativo ao núcleo

    # ===== PROPRIEDADES DA NEBLINA =====
    # Cria profundidade atmosférica e percepção de distância
    FOG_ENABLED = True
    FOG_COLOR = np.array([0.0, 0.0, 0.0, 1.0], dtype=np.float32)  # Neblina preta (escuridão)
    FOG_DENSITY = 0.1  # Espessura da neblina
    FOG_START = 4.0  # Distância onde a neblina começa (unidades)
    FOG_END = 14.0  # Distância onde a neblina é completa (unidades)

    # ===== DETECÇÃO DE COLISÃO =====
    # Parâmetros para ajuste de posição da luz perto de paredes
    COLLISION_CHECK_RADIUS = 0.15  # Raio para verificar colisões com paredes
    MIN_DISTANCE_FROM_WALL = 0.0  # Distância mínima da parede (0 = pode tocar paredes)
    DISTANCE_STEP = 0.05  # Tamanho do passo para verificação de colisão
