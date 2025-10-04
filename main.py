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
from victory_screen import VictoryScreen
from config import game_config
from light.light import LightBall
import os
import numpy as np


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


def show_victory(width, height):
    """Show the victory screen with credits."""
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption("Dreamrooms - Victory!")

    victory_screen = VictoryScreen(width, height)
    clock = pygame.time.Clock()

    while True:
        delta_time = clock.tick(60) / 1000.0

        for event in pygame.event.get():
            if event.type == QUIT:
                return 'quit'

            action = victory_screen.handle_event(event)
            if action:
                return action

        victory_screen.update(delta_time)
        victory_screen.render(screen)
        pygame.display.flip()


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

    # Create light ball
    light_ball = LightBall(distance=0.8, height_offset=-0.5, radius=0.15, light_range=15.0)

    # Game loop variables
    clock = pygame.time.Clock()
    running = True

    # Credits overlay
    credits_font = pygame.font.Font(None, 40)
    credits_lines = [
        "Credits:",
        "Sarah Mitchell - Game Director",
        "Alex Chen - Lead Programmer",
        "Marcus Rodriguez - Level Designer",
        "Emily Thompson - Sound Designer"
    ]
    show_credits = False
    credits_textures = []  # Store OpenGL textures for credits text

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

        # Get player position for enemy AI and victory check
        x, y, z = player.get_position()
        place.update(delta_time, x, z)

        # Check if player reached the exit (trigger victory once)
        if place.end_pos and not show_credits:
            exit_x, exit_y, exit_z = place.end_pos
            distance_to_exit = np.sqrt((x - exit_x)**2 + (z - exit_z)**2)
            if distance_to_exit < 2.0:  # Player is close to exit
                # Victory! Start outro music and show credits overlay
                show_credits = True
                autro_path = "assets/audio/autro.mp3"
                if os.path.exists(autro_path):
                    try:
                        pygame.mixer.music.load(autro_path)
                        pygame.mixer.music.play(-1)
                    except Exception as e:
                        print(f"Could not load outro music: {e}")

                # Generate text textures for credits
                credits_textures = []
                title_font = pygame.font.Font(None, 60)
                title_surf = title_font.render("VICTORY!", True, (255, 215, 0))
                credits_textures.append(('title', title_surf))

                for line in credits_lines:
                    text_surf = credits_font.render(line, True, (200, 200, 200))
                    credits_textures.append(('line', text_surf))

                # Convert pygame surfaces to OpenGL textures
                for i, (text_type, surf) in enumerate(credits_textures):
                    texture_data = pygame.image.tostring(surf, "RGBA", True)
                    tex_width = surf.get_width()
                    tex_height = surf.get_height()

                    texture_id = glGenTextures(1)
                    glBindTexture(GL_TEXTURE_2D, texture_id)
                    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
                    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
                    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, tex_width, tex_height, 0, GL_RGBA, GL_UNSIGNED_BYTE, texture_data)

                    credits_textures[i] = (text_type, texture_id, tex_width, tex_height)

        # Render
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glLoadIdentity()

        # Apply camera transformations
        pitch, yaw = player.get_view_matrix_rotation()
        glRotatef(pitch, 1, 0, 0)
        glRotatef(yaw, 0, 1, 0)

        glTranslatef(-x, -y, -z)

        # Update and render light ball (sets up lighting and renders the glowing orb)
        # If victory, set max ambient light to reveal the entire maze
        if show_credits:
            glEnable(GL_LIGHTING)
            glEnable(GL_LIGHT0)
            glLightModelfv(GL_LIGHT_MODEL_AMBIENT, [1.0, 1.0, 1.0, 1.0])  # Max ambient
            glLightfv(GL_LIGHT0, GL_DIFFUSE, [0.0, 0.0, 0.0, 1.0])  # Disable spotlight
            glEnable(GL_COLOR_MATERIAL)
            glColorMaterial(GL_FRONT_AND_BACK, GL_AMBIENT_AND_DIFFUSE)
        else:
            light_ball.update_and_render(x, y, z, yaw, pitch, collision_check=place.framework.check_collision)

        # Render the scene
        place.render()

        # Render enemy (needs to be rendered separately for billboard)
        place.render_enemy(x, z)

        # Disable lighting before UI rendering
        if not show_credits:
            light_ball.disable_lighting()
        else:
            glDisable(GL_LIGHTING)
            glDisable(GL_LIGHT0)

        # Draw credits overlay if victory triggered (2D overlay using OpenGL)
        if show_credits and credits_textures:
            # Switch to 2D orthographic projection
            glMatrixMode(GL_PROJECTION)
            glPushMatrix()
            glLoadIdentity()
            glOrtho(0, width, height, 0, -1, 1)
            glMatrixMode(GL_MODELVIEW)
            glPushMatrix()
            glLoadIdentity()

            # Disable depth test for 2D overlay
            glDisable(GL_DEPTH_TEST)

            # Draw semi-transparent background box
            glEnable(GL_BLEND)
            glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
            glColor4f(0.0, 0.0, 0.0, 0.8)
            glBegin(GL_QUADS)
            glVertex2f(50, 50)
            glVertex2f(width - 50, 50)
            glVertex2f(width - 50, 350)
            glVertex2f(50, 350)
            glEnd()

            # Enable texturing
            glEnable(GL_TEXTURE_2D)
            glColor4f(1.0, 1.0, 1.0, 1.0)

            # Draw text textures
            y_pos = 70
            for text_type, texture_id, tex_width, tex_height in credits_textures:
                glBindTexture(GL_TEXTURE_2D, texture_id)

                x_pos = width // 2 - tex_width // 2  # Center text

                glBegin(GL_QUADS)
                glTexCoord2f(0, 1)
                glVertex2f(x_pos, y_pos)
                glTexCoord2f(1, 1)
                glVertex2f(x_pos + tex_width, y_pos)
                glTexCoord2f(1, 0)
                glVertex2f(x_pos + tex_width, y_pos + tex_height)
                glTexCoord2f(0, 0)
                glVertex2f(x_pos, y_pos + tex_height)
                glEnd()

                if text_type == 'title':
                    y_pos += tex_height + 20
                else:
                    y_pos += tex_height + 10

            glDisable(GL_TEXTURE_2D)
            glDisable(GL_BLEND)

            # Restore 3D projection
            glPopMatrix()
            glMatrixMode(GL_PROJECTION)
            glPopMatrix()
            glMatrixMode(GL_MODELVIEW)

            # Re-enable depth test
            glEnable(GL_DEPTH_TEST)

        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    main()
