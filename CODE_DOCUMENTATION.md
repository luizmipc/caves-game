# Dreamrooms - Code Documentation

## Table of Contents
1. [Architecture Overview](#architecture-overview)
2. [Directory Structure](#directory-structure)
3. [Core Systems](#core-systems)
4. [Module Reference](#module-reference)
5. [Data Flow](#data-flow)
6. [Key Algorithms](#key-algorithms)

---

## Architecture Overview

**Dreamrooms** is built using Python with PyOpenGL for 3D rendering and Pygame for window management, input handling, and audio. The architecture follows a modular design pattern with clear separation of concerns:

- **Rendering**: OpenGL fixed-function pipeline for 3D graphics
- **Game Loop**: Traditional game loop in `main.py`
- **Entity-Component**: Modular systems for player, enemy, lighting, and environment
- **Procedural Generation**: Maze generation using Prim's algorithm
- **State Management**: Game states (menu, playing, victory, game over)

### Technology Stack
- **Python 3.x**: Core language
- **PyOpenGL**: 3D rendering
- **Pygame**: Window, input, audio
- **NumPy**: Mathematical operations

---

## Directory Structure

```
caves-game/
├── main.py                 # Main entry point and game loop
├── config.py               # Global game configuration
├── menu.py                 # Main menu UI
├── config_screen.py        # Settings menu UI
├── victory_screen.py       # Victory screen UI
│
├── player/                 # Player-related modules
│   ├── player.py          # Player entity and movement
│   ├── player_enemy.py    # Enemy AI entity
│   ├── movement.py        # Movement physics
│   └── lantern.py         # Unused lantern system
│
├── place/                  # Environment/world modules
│   ├── place.py           # Main world container
│   ├── framework.py       # Rendering and collision framework
│   ├── floor.py           # Floor rendering
│   ├── wall.py            # Wall rendering
│   ├── ceiling.py         # Ceiling rendering
│   └── outside.py         # Outdoor environment (grass, sky, boundary)
│
├── light/                  # Lighting system modules
│   ├── light.py           # Main light ball entity
│   ├── lighting_config.py # Lighting configuration parameters
│   ├── light_setup.py     # OpenGL lighting setup
│   ├── light_math.py      # Light math calculations
│   ├── light_renderer.py  # Light ball rendering
│   └── advanced_lighting.py # Shader-based advanced lighting (unused)
│
├── maze/                   # Maze generation modules
│   ├── maze.py            # Maze data structure and builder
│   └── generator.py       # Prim's algorithm maze generator
│
├── enemy/                  # Enemy modules
│   └── enemy.py           # Enemy entity (sphere-based, unused)
│
├── collision/              # Collision detection
│   └── framework.py       # Collision interface
│
├── spawn/                  # Spawn utilities
│   └── spawn.py           # Position calculation helpers
│
└── assets/                 # Game assets
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

## Core Systems

### 1. Game Loop (`main.py`)

The main game loop follows this structure:

```
Initialization
├── Pygame/OpenGL setup
├── Menu system
├── World generation
└── Player/Enemy spawning

Game Loop
├── Event Handling (input)
├── Update (physics, AI, collisions)
├── Render (3D scene, UI overlay)
└── Frame timing (60 FPS)

Cleanup
└── Pygame quit
```

**Key States:**
- `running`: Game is active
- `game_over`: Player was caught
- `show_credits`: Victory or game over overlay

### 2. Lighting System (`light/`)

The lighting system uses OpenGL fixed-function pipeline with a spotlight model:

**Components:**
- `LightBall`: Main light entity
- `LightingConfig`: All lighting parameters
- `LightingSetup`: OpenGL state configuration
- `LightRenderer`: Visual light ball rendering

**Features:**
- Warm torch-like color temperature
- Distance attenuation (inverse-square law)
- Spotlight with soft edges
- Fog for atmospheric depth
- Material properties for realistic surface interaction

### 3. Maze Generation (`maze/`)

**Algorithm**: Prim's Minimum Spanning Tree
- Creates perfect mazes (one path between any two points)
- Guaranteed solution from start to exit
- Dead ends for enemy spawning

**Process:**
1. Initialize grid with all walls
2. Choose random start cell
3. Use Prim's algorithm to carve passages
4. Mark start (S) and exit (E) positions
5. Find dead ends for enemy placement

### 4. Player System (`player/`)

**Movement:**
- WASD keyboard input
- Mouse look (yaw/pitch)
- Collision detection with walls
- Smooth physics with delta time

**Camera:**
- First-person perspective
- 45° FOV
- View matrix updates based on rotation

### 5. Enemy AI (`player/player_enemy.py`)

**Behavior:**
- Detection range: 15 units (sphere)
- Chase speed: 3.5 units/sec
- Pathfinding: Direct pursuit with wall collision
- Catch distance: < 1 unit triggers game over

**States:**
- Idle: Waiting to detect player
- Chasing: Pursuing player relentlessly

### 6. Rendering Pipeline

**3D Rendering:**
1. Clear buffers (color, depth)
2. Setup camera (view matrix)
3. Configure lighting
4. Render environment (floor, walls, ceiling, outside)
5. Render enemy (billboard sprite)
6. Disable lighting

**2D Overlay:**
1. Switch to orthographic projection
2. Render semi-transparent background
3. Render text textures (victory/game over)
4. Restore 3D projection

---

## Module Reference

### `main.py`
**Purpose**: Entry point, game loop, state management

**Key Functions:**
- `main()`: Main game loop
- `show_menu()`: Display main menu
- `show_config()`: Display configuration screen
- `show_victory()`: Display victory screen
- `setup_opengl()`: Initialize OpenGL settings

**Game States:**
- Menu → Config/Play
- Play → Victory/Game Over → Exit

### `config.py`
**Purpose**: Global game configuration

**Settings:**
- `music_enabled`: Toggle music on/off
- `music_volume`: Volume level (0.0-1.0)
- `maze_size`: Maze dimensions (1-10)

### `player/player.py`
**Purpose**: Player entity with movement and camera

**Key Methods:**
- `update()`: Update position with physics and collision
- `handle_key_down/up()`: Process keyboard input
- `handle_mouse_motion()`: Process mouse look
- `get_position()`: Return current position
- `get_view_matrix_rotation()`: Return camera rotation

### `place/place.py`
**Purpose**: World container, environment setup

**Responsibilities:**
- Initialize framework
- Generate and build maze
- Spawn enemy
- Update enemy AI
- Coordinate rendering

### `light/light.py`
**Purpose**: Main light source entity

**Key Methods:**
- `calculate_position()`: Position light based on player view
- `setup_lighting()`: Configure OpenGL lighting
- `render_ball()`: Draw glowing sphere
- `update_and_render()`: All-in-one update method

### `light/lighting_config.py`
**Purpose**: Centralized lighting parameters

**Categories:**
- Light ball properties (position, size, range)
- Spotlight properties (angle, exponent)
- Light colors (diffuse, ambient, specular)
- Attenuation (constant, linear, quadratic)
- Material properties (how surfaces react to light)
- Fog properties (depth perception)

### `maze/generator.py`
**Purpose**: Maze generation using Prim's algorithm

**Key Functions:**
- `generate()`: Main generation entry point
- `_prim_algorithm()`: Core maze carving
- `_get_neighbors()`: Find adjacent cells
- `find_dead_ends()`: Locate dead ends for enemy spawn

### `player/player_enemy.py`
**Purpose**: Enemy AI with billboard rendering

**Key Methods:**
- `can_see_player()`: Detection range check
- `update()`: AI logic and movement, returns True if caught player
- `render()`: Billboard sprite facing player

---

## Data Flow

### Startup Sequence
```
main()
├── pygame.init()
├── show_menu() → User selects Play
├── OpenGL setup
├── Place.__init__()
│   ├── Maze.generate() → Grid
│   ├── Maze.build() → Walls/Floor/Ceiling
│   └── Spawn enemy in dead end
├── Player.__init__() → Spawn at start position
└── LightBall.__init__()
```

### Game Loop Data Flow
```
Event Input
├── KEYDOWN/KEYUP → Player.handle_key_*()
├── MOUSEMOTION → Player.handle_mouse_motion()
└── ESC → Exit

Update Phase
├── Player.update() → Movement + Collision
├── Place.update()
│   └── Enemy.update() → AI + Collision → Returns caught status
└── LightBall.update_and_render() → Lighting setup

Render Phase
├── Camera transform (pitch, yaw, position)
├── LightBall.setup_lighting() → OpenGL lights
├── Place.render() → Environment
├── Place.render_enemy() → Enemy billboard
└── UI overlay (if game over or victory)
```

### Victory/Game Over Flow
```
Victory:
├── Player reaches exit position
├── Stop gameplay updates
├── Load autro.mp3
├── Generate victory text textures
├── Show credits overlay
└── Continue rendering (frozen state)

Game Over:
├── Enemy catches player (distance < 1.0)
├── Set game_over = True
├── Load death.mp3
├── Generate "GAME OVER" texture
├── Show overlay
├── Freeze all updates
└── Only ESC works
```

---

## Key Algorithms

### Maze Generation (Prim's Algorithm)

```python
def _prim_algorithm(grid, start_row, start_col):
    # Initialize
    walls = []
    grid[start_row][start_col] = ' '  # Mark as passage

    # Add walls of start cell
    walls.extend(get_neighbors(start_row, start_col))

    while walls:
        # Pick random wall
        current = random.choice(walls)

        # If connects passage to unvisited cell
        if is_valid_carve(current):
            # Carve passage
            grid[current.row][current.col] = ' '

            # Add new walls
            walls.extend(get_neighbors(current))

        # Remove processed wall
        walls.remove(current)
```

**Why Prim's?**
- Generates "perfect" mazes (no loops, single solution)
- Random wall selection creates organic-looking layouts
- Guaranteed solvability

### Collision Detection

```python
def check_collision(point_x, point_z, radius):
    for wall in walls:
        # Calculate closest point on wall to player
        closest_x = clamp(point_x, wall.min_x, wall.max_x)
        closest_z = clamp(point_z, wall.min_z, wall.max_z)

        # Check distance
        distance_sq = (point_x - closest_x)² + (point_z - closest_z)²

        if distance_sq < radius²:
            return True  # Collision!

    return False  # No collision
```

**Features:**
- Circle-to-AABB (Axis-Aligned Bounding Box) collision
- Finds closest point on rectangle to circle center
- Early exit on first collision found

### Light Attenuation

```python
def calculate_attenuation(distance):
    attenuation = 1.0 / (
        constant_atten +
        linear_atten * distance +
        quadratic_atten * distance²
    )
    return attenuation
```

**Formula**: Inverse-square law approximation
- **Constant**: Base brightness
- **Linear**: Gradual falloff
- **Quadratic**: Realistic distance-based dimming

### Spotlight Calculation

```python
def spotlight_effect(light_dir, spot_dir, cutoff_angle, exponent):
    # Calculate angle between light direction and spotlight direction
    cos_angle = dot(light_dir, spot_dir)

    # Check if within cone
    if acos(cos_angle) < cutoff_angle:
        # Calculate intensity with smooth falloff
        intensity = (1.0 - angle/cutoff_angle) ** exponent
        return intensity
    else:
        return 0.0  # Outside cone, no light
```

**Features:**
- Smooth cone edges (exponent controls smoothness)
- Angular falloff for realistic spotlight behavior

---

## Performance Considerations

### Optimization Strategies

1. **Collision Detection**
   - Grid-based spatial partitioning (walls organized by cell)
   - Early exit on first collision
   - Smaller collision radius for enemies (0.3 vs 0.5)

2. **Rendering**
   - Fixed-function pipeline (no shader compilation overhead)
   - Minimal state changes
   - Batched geometry (single quad per wall face)
   - Texture clamping to avoid repeat overhead

3. **Maze Generation**
   - One-time generation at startup
   - Efficient grid representation (2D array)
   - Dead end caching for enemy spawn

4. **Update Loop**
   - Delta time for frame-rate independence
   - Conditional updates (no updates when game over)
   - Single enemy instance

### Potential Bottlenecks

- **Large mazes**: O(n²) collision checks with many walls
- **Fog rendering**: Per-pixel calculation in fixed-function
- **Text texture generation**: String rendering to texture conversion

### Scalability

Current design supports:
- Maze sizes up to 10x10 comfortably
- Single enemy (could extend to multiple with spatial partitioning)
- 60 FPS target on modest hardware

---

## Extension Points

### Adding New Features

**Multiple Enemies:**
```python
# In place/place.py
self.enemies = [PlayerEnemy(...) for _ in range(num_enemies)]

def update(self, delta_time, player_x, player_z):
    for enemy in self.enemies:
        if enemy.update(delta_time, player_x, player_z, collision_check):
            return True  # Any enemy caught player
    return False
```

**Power-ups:**
```python
# Create new module: items/powerup.py
class Powerup:
    def __init__(self, x, z, effect_type):
        self.position = (x, z)
        self.type = effect_type  # 'speed', 'light_boost', etc.

    def apply(self, player):
        if self.type == 'speed':
            player.speed *= 1.5
```

**Sound Effects:**
```python
# In player.py
footstep_sound = pygame.mixer.Sound('assets/audio/footstep.wav')

def update(self, delta_time):
    if moving:
        if step_timer > step_interval:
            footstep_sound.play()
            step_timer = 0
```

---

## Debugging Tips

### Common Issues

**Light not working:**
- Check `glEnable(GL_LIGHTING)` is called
- Verify normals are set correctly (glNormal3f)
- Ensure material properties are configured

**Collisions not working:**
- Print collision radius and positions
- Visualize collision boxes with debug rendering
- Check coordinate system (OpenGL Y-up vs grid row/col)

**Maze unsolvable:**
- Verify Prim's algorithm completion
- Check start/exit positions are in passages (' ')
- Print maze grid to console

**Performance issues:**
- Profile with Python's `cProfile`
- Check maze size configuration
- Monitor frame time with `clock.tick()`

### Debug Rendering

```python
# Add to render() in place/framework.py
def render_debug_collision_boxes(self):
    glDisable(GL_LIGHTING)
    glColor3f(1, 0, 0)  # Red wireframe
    for wall in self.walls:
        # Draw wireframe box for each wall
        draw_wireframe_box(wall.x, wall.z, wall.width, wall.depth)
    glEnable(GL_LIGHTING)
```

---

## Code Style and Conventions

### Naming Conventions
- **Classes**: PascalCase (`PlayerEnemy`, `LightBall`)
- **Functions/Methods**: snake_case (`update_and_render`, `check_collision`)
- **Constants**: UPPER_SNAKE_CASE (`SPOT_CUTOFF_ANGLE`, `TEXTURE_PATH`)
- **Private Methods**: Leading underscore (`_load_texture`, `_prim_algorithm`)

### Documentation
- Docstrings for all classes and public methods
- Type hints in function signatures where helpful
- Comments for complex algorithms

### File Organization
- One class per file (with exceptions for small helpers)
- Related classes grouped in directories
- Configuration separated from logic

---

## Dependencies and Versions

### Required Libraries
```
pygame>=2.0.0        # Window, input, audio
PyOpenGL>=3.1.0      # 3D rendering
PyOpenGL-accelerate  # Performance boost
numpy>=1.20.0        # Math operations
```

### Python Version
- Minimum: Python 3.7
- Recommended: Python 3.9+

---

## Future Improvements

### Potential Enhancements
1. **Shader-based lighting**: More realistic illumination (currently has basic implementation in `advanced_lighting.py`)
2. **Procedural textures**: Generate textures at runtime
3. **Multiple floors**: Vertical maze navigation
4. **Save system**: Checkpoint progress
5. **Difficulty modes**: Adjust enemy speed, detection range, maze size
6. **Audio effects**: Footsteps, breathing, enemy sounds
7. **Particle effects**: Dust, atmospheric effects
8. **Minimap**: Optional navigation aid (unlockable?)

---

**Note**: This documentation reflects the current state of the codebase. As the game evolves, keep this document updated to reflect architectural changes and new systems.
