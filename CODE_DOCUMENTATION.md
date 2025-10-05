# Dreamrooms - Documentação do Código

## Índice
1. [Visão Geral da Arquitetura](#visão-geral-da-arquitetura)
2. [Estrutura de Diretórios](#estrutura-de-diretórios)
3. [Sistemas Principais](#sistemas-principais)
4. [Referência de Módulos](#referência-de-módulos)
5. [Fluxo de Dados](#fluxo-de-dados)
6. [Algoritmos Principais](#algoritmos-principais)

---

## Visão Geral da Arquitetura

**Dreamrooms** é construído usando Python com PyOpenGL para renderização 3D e Pygame para gerenciamento de janelas, entrada e áudio. A arquitetura segue um padrão de design modular com clara separação de responsabilidades:

- **Renderização**: Pipeline de função fixa OpenGL para gráficos 3D
- **Loop do Jogo**: Loop de jogo tradicional em `main.py`
- **Entidade-Componente**: Sistemas modulares para jogador, inimigo, iluminação e ambiente
- **Geração Procedural**: Geração de labirinto usando o algoritmo de Prim
- **Gerenciamento de Estado**: Estados do jogo (menu, jogando, vitória, game over)

### Stack de Tecnologia
- **Python 3.x**: Linguagem principal
- **PyOpenGL**: Renderização 3D
- **Pygame**: Janela, entrada, áudio
- **NumPy**: Operações matemáticas

---

## Estrutura de Diretórios

```
caves-game/
├── main.py                 # Ponto de entrada principal e loop do jogo
├── config.py               # Configuração global do jogo
├── menu.py                 # UI do menu principal
├── config_screen.py        # UI do menu de configurações
├── victory_screen.py       # UI da tela de vitória
│
├── player/                 # Módulos relacionados ao jogador
│   ├── player.py          # Entidade do jogador e movimento
│   ├── player_enemy.py    # Entidade da IA inimiga
│   ├── movement.py        # Física de movimento
│   └── lantern.py         # Sistema de lanterna não utilizado
│
├── place/                  # Módulos de ambiente/mundo
│   ├── place.py           # Container principal do mundo
│   ├── framework.py       # Framework de renderização e colisão
│   ├── floor.py           # Renderização do chão
│   ├── wall.py            # Renderização das paredes
│   ├── ceiling.py         # Renderização do teto
│   └── outside.py         # Ambiente externo (grama, céu, limite)
│
├── light/                  # Módulos do sistema de iluminação
│   ├── light.py           # Entidade principal da bola de luz
│   ├── lighting_config.py # Parâmetros de configuração de iluminação
│   ├── light_setup.py     # Configuração de iluminação OpenGL
│   ├── light_math.py      # Cálculos matemáticos de luz
│   ├── light_renderer.py  # Renderização da bola de luz
│   └── advanced_lighting.py # Iluminação avançada baseada em shaders (não utilizada)
│
├── maze/                   # Módulos de geração de labirinto
│   ├── maze.py            # Estrutura de dados e construtor do labirinto
│   └── generator.py       # Gerador de labirinto com algoritmo de Prim
│
├── enemy/                  # Módulos de inimigo
│   └── enemy.py           # Entidade inimiga (baseada em esfera, não utilizada)
│
├── collision/              # Detecção de colisão
│   └── framework.py       # Interface de colisão
│
├── spawn/                  # Utilitários de spawn
│   └── spawn.py           # Auxiliares de cálculo de posição
│
└── assets/                 # Recursos do jogo
    ├── audio/
    │   ├── soundtrack.mp3
    │   ├── autro.mp3
    │   └── death.mp3
    └── textures/
        ├── floor.png
        ├── wall.png
        └── enemy.png
```

---

## Sistemas Principais

### 1. Loop do Jogo (`main.py`)

O loop principal do jogo segue esta estrutura:

```
Inicialização
├── Configuração Pygame/OpenGL
├── Sistema de menu
├── Geração do mundo
└── Spawn do jogador/inimigo

Loop do Jogo
├── Tratamento de Eventos (entrada)
├── Atualização (física, IA, colisões)
├── Renderização (cena 3D, sobreposição UI)
└── Temporização de frames (60 FPS)

Limpeza
└── Encerramento do Pygame
```

**Estados Principais:**
- `running`: Jogo está ativo
- `game_over`: Jogador foi capturado
- `show_credits`: Sobreposição de vitória ou game over

### 2. Sistema de Iluminação (`light/`)

O sistema de iluminação usa o pipeline de função fixa OpenGL com um modelo de holofote:

**Componentes:**
- `LightBall`: Entidade de luz principal
- `LightingConfig`: Todos os parâmetros de iluminação
- `LightingSetup`: Configuração de estado OpenGL
- `LightRenderer`: Renderização visual da bola de luz

**Recursos:**
- Temperatura de cor quente semelhante a tocha
- Atenuação por distância (lei do inverso do quadrado)
- Holofote com bordas suaves
- Neblina para profundidade atmosférica
- Propriedades de material para interação realista de superfície

### 3. Geração de Labirinto (`maze/`)

**Algoritmo**: Árvore Geradora Mínima de Prim
- Cria labirintos perfeitos (um caminho entre quaisquer dois pontos)
- Solução garantida do início à saída
- Becos sem saída para spawn de inimigos

**Processo:**
1. Inicializar grade com todas as paredes
2. Escolher célula inicial aleatória
3. Usar algoritmo de Prim para esculpir passagens
4. Marcar posições de início (S) e saída (E)
5. Encontrar becos sem saída para colocação de inimigos

### 4. Sistema do Jogador (`player/`)

**Movimento:**
- Entrada de teclado WASD
- Visão com mouse (yaw/pitch)
- Detecção de colisão com paredes
- Física suave com delta time

**Câmera:**
- Perspectiva em primeira pessoa
- FOV de 45°
- Matriz de visão atualizada com base na rotação

### 5. IA do Inimigo (`player/player_enemy.py`)

**Comportamento:**
- Alcance de detecção: 15 unidades (esfera)
- Velocidade de perseguição: 3.5 unidades/seg
- Pathfinding: Perseguição direta com colisão de parede
- Distância de captura: < 1 unidade dispara game over

**Estados:**
- Inativo: Aguardando para detectar jogador
- Perseguindo: Perseguindo jogador implacavelmente

### 6. Pipeline de Renderização

**Renderização 3D:**
1. Limpar buffers (cor, profundidade)
2. Configurar câmera (matriz de visão)
3. Configurar iluminação
4. Renderizar ambiente (chão, paredes, teto, externo)
5. Renderizar inimigo (sprite billboard)
6. Desabilitar iluminação

**Sobreposição 2D:**
1. Mudar para projeção ortográfica
2. Renderizar fundo semi-transparente
3. Renderizar texturas de texto (vitória/game over)
4. Restaurar projeção 3D

---

## Referência de Módulos

### `main.py`
**Propósito**: Ponto de entrada, loop do jogo, gerenciamento de estado

**Funções Principais:**
- `main()`: Loop principal do jogo
- `show_menu()`: Exibir menu principal
- `show_config()`: Exibir tela de configuração
- `show_victory()`: Exibir tela de vitória
- `setup_opengl()`: Inicializar configurações OpenGL

**Estados do Jogo:**
- Menu → Config/Jogar
- Jogar → Vitória/Game Over → Sair

### `config.py`
**Propósito**: Configuração global do jogo

**Configurações:**
- `music_enabled`: Ativar/desativar música
- `music_volume`: Nível de volume (0.0-1.0)
- `maze_size`: Dimensões do labirinto (1-10)

### `player/player.py`
**Propósito**: Entidade do jogador com movimento e câmera

**Métodos Principais:**
- `update()`: Atualizar posição com física e colisão
- `handle_key_down/up()`: Processar entrada de teclado
- `handle_mouse_motion()`: Processar visão com mouse
- `get_position()`: Retornar posição atual
- `get_view_matrix_rotation()`: Retornar rotação da câmera

### `place/place.py`
**Propósito**: Container do mundo, configuração do ambiente

**Responsabilidades:**
- Inicializar framework
- Gerar e construir labirinto
- Spawn do inimigo
- Atualizar IA do inimigo
- Coordenar renderização

### `light/light.py`
**Propósito**: Entidade da fonte de luz principal

**Métodos Principais:**
- `calculate_position()`: Posicionar luz baseada na visão do jogador
- `setup_lighting()`: Configurar iluminação OpenGL
- `render_ball()`: Desenhar esfera brilhante
- `update_and_render()`: Método de atualização tudo-em-um

### `light/lighting_config.py`
**Propósito**: Parâmetros de iluminação centralizados

**Categorias:**
- Propriedades da bola de luz (posição, tamanho, alcance)
- Propriedades do holofote (ângulo, expoente)
- Cores da luz (difusa, ambiente, especular)
- Atenuação (constante, linear, quadrática)
- Propriedades de material (como superfícies reagem à luz)
- Propriedades de neblina (percepção de profundidade)

### `maze/generator.py`
**Propósito**: Geração de labirinto usando algoritmo de Prim

**Funções Principais:**
- `generate()`: Ponto de entrada principal da geração
- `_prim_algorithm()`: Núcleo de esculpir labirinto
- `_get_neighbors()`: Encontrar células adjacentes
- `find_dead_ends()`: Localizar becos sem saída para spawn de inimigo

### `player/player_enemy.py`
**Propósito**: IA do inimigo com renderização billboard

**Métodos Principais:**
- `can_see_player()`: Verificação de alcance de detecção
- `update()`: Lógica de IA e movimento, retorna True se capturou jogador
- `render()`: Sprite billboard voltado para o jogador

---

## Fluxo de Dados

### Sequência de Inicialização
```
main()
├── pygame.init()
├── show_menu() → Usuário seleciona Jogar
├── Configuração OpenGL
├── Place.__init__()
│   ├── Maze.generate() → Grade
│   ├── Maze.build() → Paredes/Chão/Teto
│   └── Spawn inimigo em beco sem saída
├── Player.__init__() → Spawn na posição inicial
└── LightBall.__init__()
```

### Fluxo de Dados do Loop do Jogo
```
Entrada de Evento
├── KEYDOWN/KEYUP → Player.handle_key_*()
├── MOUSEMOTION → Player.handle_mouse_motion()
└── ESC → Sair

Fase de Atualização
├── Player.update() → Movimento + Colisão
├── Place.update()
│   └── Enemy.update() → IA + Colisão → Retorna status de captura
└── LightBall.update_and_render() → Configuração de iluminação

Fase de Renderização
├── Transformação da câmera (pitch, yaw, posição)
├── LightBall.setup_lighting() → Luzes OpenGL
├── Place.render() → Ambiente
├── Place.render_enemy() → Billboard do inimigo
└── Sobreposição UI (se game over ou vitória)
```

### Fluxo de Vitória/Game Over
```
Vitória:
├── Jogador alcança posição de saída
├── Parar atualizações do gameplay
├── Carregar autro.mp3
├── Gerar texturas de texto de vitória
├── Mostrar sobreposição de créditos
└── Continuar renderizando (estado congelado)

Game Over:
├── Inimigo captura jogador (distância < 1.0)
├── Definir game_over = True
├── Carregar death.mp3
├── Gerar textura "GAME OVER"
├── Mostrar sobreposição
├── Congelar todas as atualizações
└── Apenas ESC funciona
```

---

## Algoritmos Principais

### Geração de Labirinto (Algoritmo de Prim)

```python
def _prim_algorithm(grid, start_row, start_col):
    # Inicializar
    walls = []
    grid[start_row][start_col] = ' '  # Marcar como passagem

    # Adicionar paredes da célula inicial
    walls.extend(get_neighbors(start_row, start_col))

    while walls:
        # Escolher parede aleatória
        current = random.choice(walls)

        # Se conecta passagem a célula não visitada
        if is_valid_carve(current):
            # Esculpir passagem
            grid[current.row][current.col] = ' '

            # Adicionar novas paredes
            walls.extend(get_neighbors(current))

        # Remover parede processada
        walls.remove(current)
```

**Por que Prim?**
- Gera labirintos "perfeitos" (sem loops, solução única)
- Seleção de parede aleatória cria layouts de aparência orgânica
- Resolubilidade garantida

### Detecção de Colisão

```python
def check_collision(point_x, point_z, radius):
    for wall in walls:
        # Calcular ponto mais próximo na parede ao jogador
        closest_x = clamp(point_x, wall.min_x, wall.max_x)
        closest_z = clamp(point_z, wall.min_z, wall.max_z)

        # Verificar distância
        distance_sq = (point_x - closest_x)² + (point_z - closest_z)²

        if distance_sq < radius²:
            return True  # Colisão!

    return False  # Sem colisão
```

**Recursos:**
- Colisão Círculo-para-AABB (Axis-Aligned Bounding Box)
- Encontra ponto mais próximo no retângulo ao centro do círculo
- Saída antecipada na primeira colisão encontrada

### Atenuação de Luz

```python
def calculate_attenuation(distance):
    attenuation = 1.0 / (
        constant_atten +
        linear_atten * distance +
        quadratic_atten * distance²
    )
    return attenuation
```

**Fórmula**: Aproximação da lei do inverso do quadrado
- **Constante**: Brilho base
- **Linear**: Queda gradual
- **Quadrática**: Escurecimento realista baseado em distância

### Cálculo de Holofote

```python
def spotlight_effect(light_dir, spot_dir, cutoff_angle, exponent):
    # Calcular ângulo entre direção da luz e direção do holofote
    cos_angle = dot(light_dir, spot_dir)

    # Verificar se está dentro do cone
    if acos(cos_angle) < cutoff_angle:
        # Calcular intensidade com queda suave
        intensity = (1.0 - angle/cutoff_angle) ** exponent
        return intensity
    else:
        return 0.0  # Fora do cone, sem luz
```

**Recursos:**
- Bordas de cone suaves (expoente controla suavidade)
- Queda angular para comportamento realista de holofote

---

## Considerações de Performance

### Estratégias de Otimização

1. **Detecção de Colisão**
   - Particionamento espacial baseado em grade (paredes organizadas por célula)
   - Saída antecipada na primeira colisão
   - Raio de colisão menor para inimigos (0.3 vs 0.5)

2. **Renderização**
   - Pipeline de função fixa (sem overhead de compilação de shader)
   - Mudanças de estado mínimas
   - Geometria em lote (único quad por face de parede)
   - Clamping de textura para evitar overhead de repetição

3. **Geração de Labirinto**
   - Geração única na inicialização
   - Representação eficiente de grade (array 2D)
   - Cache de becos sem saída para spawn de inimigo

4. **Loop de Atualização**
   - Delta time para independência de taxa de frames
   - Atualizações condicionais (sem atualizações quando game over)
   - Instância única de inimigo

### Gargalos Potenciais

- **Labirintos grandes**: Verificações de colisão O(n²) com muitas paredes
- **Renderização de neblina**: Cálculo por pixel em função fixa
- **Geração de textura de texto**: Conversão de renderização de string para textura

### Escalabilidade

O design atual suporta:
- Tamanhos de labirinto até 10x10 confortavelmente
- Inimigo único (poderia estender para múltiplos com particionamento espacial)
- Alvo de 60 FPS em hardware modesto

---

## Pontos de Extensão

### Adicionando Novos Recursos

**Múltiplos Inimigos:**
```python
# Em place/place.py
self.enemies = [PlayerEnemy(...) for _ in range(num_enemies)]

def update(self, delta_time, player_x, player_z):
    for enemy in self.enemies:
        if enemy.update(delta_time, player_x, player_z, collision_check):
            return True  # Qualquer inimigo capturou jogador
    return False
```

**Power-ups:**
```python
# Criar novo módulo: items/powerup.py
class Powerup:
    def __init__(self, x, z, effect_type):
        self.position = (x, z)
        self.type = effect_type  # 'speed', 'light_boost', etc.

    def apply(self, player):
        if self.type == 'speed':
            player.speed *= 1.5
```

**Efeitos Sonoros:**
```python
# Em player.py
footstep_sound = pygame.mixer.Sound('assets/audio/footstep.wav')

def update(self, delta_time):
    if moving:
        if step_timer > step_interval:
            footstep_sound.play()
            step_timer = 0
```

---

## Dicas de Depuração

### Problemas Comuns

**Luz não funcionando:**
- Verificar se `glEnable(GL_LIGHTING)` está chamado
- Verificar se normais estão configuradas corretamente (glNormal3f)
- Garantir que propriedades de material estejam configuradas

**Colisões não funcionando:**
- Imprimir raio de colisão e posições
- Visualizar caixas de colisão com renderização de debug
- Verificar sistema de coordenadas (OpenGL Y-up vs linha/coluna da grade)

**Labirinto insolúvel:**
- Verificar conclusão do algoritmo de Prim
- Verificar se posições de início/saída estão em passagens (' ')
- Imprimir grade do labirinto no console

**Problemas de performance:**
- Perfilar com `cProfile` do Python
- Verificar configuração de tamanho do labirinto
- Monitorar tempo de frame com `clock.tick()`

### Renderização de Debug

```python
# Adicionar a render() em place/framework.py
def render_debug_collision_boxes(self):
    glDisable(GL_LIGHTING)
    glColor3f(1, 0, 0)  # Wireframe vermelho
    for wall in self.walls:
        # Desenhar caixa wireframe para cada parede
        draw_wireframe_box(wall.x, wall.z, wall.width, wall.depth)
    glEnable(GL_LIGHTING)
```

---

## Estilo e Convenções de Código

### Convenções de Nomenclatura
- **Classes**: PascalCase (`PlayerEnemy`, `LightBall`)
- **Funções/Métodos**: snake_case (`update_and_render`, `check_collision`)
- **Constantes**: UPPER_SNAKE_CASE (`SPOT_CUTOFF_ANGLE`, `TEXTURE_PATH`)
- **Métodos Privados**: Underscore inicial (`_load_texture`, `_prim_algorithm`)

### Documentação
- Docstrings para todas as classes e métodos públicos
- Type hints em assinaturas de função quando útil
- Comentários para algoritmos complexos

### Organização de Arquivos
- Uma classe por arquivo (com exceções para pequenos auxiliares)
- Classes relacionadas agrupadas em diretórios
- Configuração separada da lógica

---

## Dependências e Versões

### Bibliotecas Necessárias
```
pygame>=2.0.0        # Janela, entrada, áudio
PyOpenGL>=3.1.0      # Renderização 3D
PyOpenGL-accelerate  # Aumento de performance
numpy>=1.20.0        # Operações matemáticas
```

### Versão do Python
- Mínimo: Python 3.7
- Recomendado: Python 3.9+

---

## Melhorias Futuras

### Aprimoramentos Potenciais
1. **Iluminação baseada em shader**: Iluminação mais realista (atualmente tem implementação básica em `advanced_lighting.py`)
2. **Texturas procedurais**: Gerar texturas em tempo de execução
3. **Múltiplos andares**: Navegação vertical no labirinto
4. **Sistema de salvamento**: Progresso de checkpoint
5. **Modos de dificuldade**: Ajustar velocidade do inimigo, alcance de detecção, tamanho do labirinto
6. **Efeitos de áudio**: Passos, respiração, sons do inimigo
7. **Efeitos de partículas**: Poeira, efeitos atmosféricos
8. **Minimapa**: Auxílio de navegação opcional (desbloqueável?)

---

**Nota**: Esta documentação reflete o estado atual do código. À medida que o jogo evolui, mantenha este documento atualizado para refletir mudanças arquiteturais e novos sistemas.
