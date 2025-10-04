#!/usr/bin/env python3
"""
Dreamrooms - A 3D maze game with first-person player movement.
Controls:
- WASD: Move around
- Mouse: Look around
- ESC: Exit
"""

import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *

from player.player import Player
from place.place import Place
from menu import Menu
from config_screen import ConfigScreen
from config import game_config
import os


SOUNDTRACK_PATH = "assets/audio/soundtrack.mp3"


def load_soundtrack():
    """Load and play soundtrack in loop if it exists."""
    if os.path.exists(SOUNDTRACK_PATH):
        try:
            pygame.mixer.init()
            pygame.mixer.music.load(SOUNDTRACK_PATH)
            pygame.mixer.music.set_volume(game_config.music_volume)
            if game_config.music_enabled:
                pygame.mixer.music.play(-1)  # -1 means loop forever
        except Exception as e:
            print(f"Could not load soundtrack: {e}")


def update_music():
    """Update music based on config settings."""
    pygame.mixer.music.set_volume(game_config.music_volume)
    if game_config.music_enabled and not pygame.mixer.music.get_busy():
        pygame.mixer.music.play(-1)
    elif not game_config.music_enabled and pygame.mixer.music.get_busy():
        pygame.mixer.music.stop()


def show_config(width, height):
    """Show the config screen and return when done."""
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption("Dreamrooms - Config")

    config_screen = ConfigScreen(width, height)
    clock = pygame.time.Clock()

    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                return 'quit'

            action = config_screen.handle_event(event)
            if action == 'back':
                return 'menu'

        # Update music settings
        update_music()

        config_screen.render(screen)
        pygame.display.flip()
        clock.tick(60)


def show_menu(width, height):
    """Show the main menu and return user choice."""
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption("Dreamrooms - Menu")

    menu = Menu(width, height)
    clock = pygame.time.Clock()

    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                return 'quit'

            action = menu.handle_event(event)
            if action:
                return action

        menu.render(screen)
        pygame.display.flip()
        clock.tick(60)


def setup_opengl(width, height):
    """Initialize OpenGL settings."""
    glEnable(GL_DEPTH_TEST)
    glViewport(0, 0, width, height)

    # Set up perspective projection with far clipping plane extended for outside environment
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(45, width / height, 0.1, 1000.0)  # Increased from 100 to 1000

    glMatrixMode(GL_MODELVIEW)


def main():
    # Initialize Pygame
    pygame.init()
    width, height = 800, 600

    # Load and play soundtrack
    load_soundtrack()

    # Menu loop
    while True:
        action = show_menu(width, height)

        if action == 'quit':
            pygame.quit()
            return
        elif action == 'config':
            config_action = show_config(width, height)
            if config_action == 'quit':
                pygame.quit()
                return
            # If 'menu', loop continues to show menu again
        elif action == 'play':
            break  # Exit menu loop and start game

    # Setup game
    pygame.display.set_mode((width, height), DOUBLEBUF | OPENGL)
    pygame.display.set_caption("Dreamrooms - WASD to move, Mouse to look")

    # Hide and capture mouse
    pygame.mouse.set_visible(False)
    pygame.event.set_grab(True)

    # Setup OpenGL
    setup_opengl(width, height)

    # Create game objects
    place = Place()

    # Use maze start position if available, otherwise default
    if place.start_pos:
        player = Player(x=place.start_pos[0], y=place.start_pos[1], z=place.start_pos[2])
    else:
        player = Player(x=0, y=1.7, z=5)

    # Game loop variables
    clock = pygame.time.Clock()
    running = True

    while running:
        # Handle events
        for event in pygame.event.get():
            if event.type == QUIT:
                running = False
            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    running = False
                else:
                    player.handle_key_down(event.key)
            elif event.type == KEYUP:
                player.handle_key_up(event.key)
            elif event.type == MOUSEMOTION:
                player.handle_mouse_motion(event.rel[0], event.rel[1])

        # Update game state
        delta_time = clock.tick(60) / 1000.0  # Convert to seconds
        player.update(delta_time, collision_check=place.framework.check_collision)

        # Get player position for enemy AI
        x, y, z = player.get_position()
        place.update(delta_time, x, z)

        # Render
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glLoadIdentity()

        # Apply camera transformations
        pitch, yaw = player.get_view_matrix_rotation()
        glRotatef(pitch, 1, 0, 0)
        glRotatef(yaw, 0, 1, 0)

        glTranslatef(-x, -y, -z)

        # Render the scene
        place.render()

        # Render enemy (needs to be rendered separately for billboard)
        place.render_enemy(x, z)

        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    main()
