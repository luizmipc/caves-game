# Dreamrooms - Player Manual

## Table of Contents
1. [Getting Started](#getting-started)
2. [Controls](#controls)
3. [Game Objectives](#game-objectives)
4. [Gameplay Mechanics](#gameplay-mechanics)
5. [Tips and Strategies](#tips-and-strategies)
6. [Configuration](#configuration)

---

## Getting Started

### System Requirements
- Python 3.x
- PyOpenGL
- pygame
- numpy

### Installation

1. **Create a virtual environment:**
```bash
python -m venv venv
```

2. **Activate the virtual environment:**
```bash
source venv/bin/activate
```

3. **Install dependencies:**
```bash
pip install -r requirements.txt
```

### Running the Game
```bash
python main.py
```

**Note**: Make sure the virtual environment is activated (you should see `(venv)` in your terminal prompt) before running the game.

### Main Menu
When you launch the game, you'll see the main menu with three options:
- **Play**: Start a new game
- **Config**: Adjust game settings (music volume, maze size)
- **Quit**: Exit the game

---

## Controls

### Movement
- **W**: Move forward
- **S**: Move backward
- **A**: Strafe left
- **D**: Strafe right

### Camera
- **Mouse Movement**: Look around (360-degree view)
- The camera follows your mouse movements for full control over your view direction

### System
- **ESC**: Exit the game (works at any time)

---

## Game Objectives

### Primary Goal
Navigate through the dark maze to find the **EXIT** before the enemy catches you.

### Victory Condition
Reach the exit point (marked location in the maze). When you escape:
- The entire maze is revealed in full light
- Victory music plays
- Credits are displayed
- You've successfully escaped the nightmare

### Defeat Condition
If the enemy catches you (gets within 1 unit of your position):
- Death music plays
- "GAME OVER" appears on screen in red
- You cannot move - only press ESC to exit
- You must restart to try again

---

## Gameplay Mechanics

### The Light Source
- You carry a torch-like light source that illuminates a cone in front of you
- **Cone angle**: 35 degrees
- **Range**: 15 units
- **Position**: The light source is positioned behind and below your eye level for immersion (you won't see it)
- The light has warm, realistic falloff with atmospheric fog

### The Maze
- **Procedurally generated**: Each playthrough creates a new maze layout
- **Size**: Configurable in settings (1-10, where higher = larger maze)
- **Layout**: Guaranteed to have a path from start to exit
- The maze includes dead ends where the enemy may spawn

### The Enemy
- **Detection Range**: 15 units - if you get within this range, the enemy will spot you
- **Chase Speed**: 3.5 units/second (faster than your walking speed)
- **AI Behavior**:
  - Patrols until it spots you
  - Once it sees you, it will chase relentlessly
  - Can navigate around walls
  - Will catch you if it gets within 1 unit
- **Spawn Location**: Randomly placed in a dead end, away from start and exit points

### Visibility
- **Darkness**: The maze is in complete darkness except for your light
- **Fog**: Distance fog creates atmospheric depth (starts at 4 units, complete at 14 units)
- **Surface Lighting**: Walls, floors, and ceilings react realistically to your light source

---

## Tips and Strategies

### Navigation
1. **Mark Your Path**: Try to remember turns and landmarks
2. **Listen Carefully**: Audio cues can help you orient yourself
3. **Check Corners**: The enemy could be around any corner
4. **Dead Ends**: If you hit a dead end, backtrack quickly

### Dealing with the Enemy
1. **Stay Alert**: Once you're within 15 units, the chase begins
2. **Keep Moving**: The enemy is faster than you - don't stop
3. **Use Corners**: Sharp turns can help you break line of sight
4. **Know Your Limits**: You can get very close to walls without the light failing

### Light Management
1. **Point Where You're Going**: The light follows your view direction
2. **Close-Range Visibility**: You can get right up against walls and still see them
3. **Wide Cone**: The 35-degree cone gives you good peripheral vision
4. **Fog Awareness**: Objects far away will fade into darkness

### General Strategy
- **Explore Systematically**: Try to follow a pattern (e.g., always turn right)
- **Don't Panic**: When chased, think about your escape route
- **Learn the Sounds**: The ambient soundtrack and audio cues are part of the experience
- **Embrace the Atmosphere**: This is a game about tension and dread - let yourself be immersed

---

## Configuration

### Settings Menu
Access the configuration menu from the main menu to adjust:

#### Music Settings
- **Music Enabled/Disabled**: Toggle background music on/off
- **Volume**: Adjust music volume (0.0 to 1.0)

#### Maze Settings
- **Maze Size**: Set the size of the generated maze (1-10)
  - Size 1-3: Small, quick games
  - Size 4-6: Medium, balanced difficulty
  - Size 7-10: Large, extended exploration

### Audio Files
The game uses three audio files (place in `assets/audio/`):
- **soundtrack.mp3**: Main game music (loops during gameplay)
- **autro.mp3**: Victory music (plays when you reach the exit)
- **death.mp3**: Game over music (plays when caught by the enemy)

If these files are missing, the game will still run but without music.

### Textures
The game can use custom textures (place in `assets/textures/`):
- **floor.png**: Floor texture
- **wall.png**: Wall texture
- **enemy.png**: Enemy sprite texture

If textures are missing, the game will use default colors.

---

## Understanding the Experience

**Dreamrooms** is designed to evoke specific feelings:

- **Liminal Dread**: The feeling of being in a transitional space that shouldn't exist
- **Isolation**: You are alone with only your light for comfort
- **Pursuit**: Something is hunting you in the darkness
- **Disorientation**: The maze is meant to confuse and unsettle

This is not a game about winning quickly. It's about the journey through the maze, the tension of exploration, and the desperate flight when discovered. Take your time, immerse yourself in the atmosphere, and remember: you're not supposed to feel safe.

---

## Troubleshooting

### Game Won't Start
- Ensure all dependencies are installed: `pip install PyOpenGL PyOpenGL_accelerate pygame numpy`
- Check Python version (3.x required)

### Performance Issues
- Lower the maze size in configuration
- Close other applications
- Update graphics drivers

### No Sound
- Check that audio files exist in `assets/audio/`
- Verify pygame mixer is installed correctly
- Check system volume settings

### Black Screen
- The game is meant to be dark! Move around and look for the light
- If truly broken, check OpenGL compatibility

---

## Credits

**Game Developers:**
- Leonardo Zordan Lima
- Luiz Marcelo Itapicuru Pereira Costa
- Matheus Soares Martins
- Thiago Crivaro Nunes

**Inspired By:**
- Backrooms/Liminal Space aesthetics
- Dreamcore visual culture
- David Lynch (Twin Peaks, Lost Highway)
- David Bowie's experimental art

---

*Good luck. You'll need it.*
