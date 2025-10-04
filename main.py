#!/usr/bin/env python3
"""
Simple 3D game with floor and first-person player movement.
Controls:
- WASD: Move around
- Mouse: Look around
- ESC: Exit
"""

import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *

from player import Player
from place import Place


def setup_opengl(width, height):
    """Initialize OpenGL settings."""
    glEnable(GL_DEPTH_TEST)
    glViewport(0, 0, width, height)

    # Set up perspective projection
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(45, width / height, 0.1, 100.0)

    glMatrixMode(GL_MODELVIEW)


def main():
    # Initialize Pygame
    pygame.init()
    width, height = 800, 600
    pygame.display.set_mode((width, height), DOUBLEBUF | OPENGL)
    pygame.display.set_caption("Caves Game - WASD to move, Mouse to look")

    # Hide and capture mouse
    pygame.mouse.set_visible(False)
    pygame.event.set_grab(True)

    # Setup OpenGL
    setup_opengl(width, height)

    # Create game objects
    player = Player(x=0, y=1.7, z=5)
    place = Place()

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
        player.update(delta_time)

        # Render
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glLoadIdentity()

        # Apply camera transformations
        pitch, yaw = player.get_view_matrix_rotation()
        glRotatef(pitch, 1, 0, 0)
        glRotatef(yaw, 0, 1, 0)

        x, y, z = player.get_position()
        glTranslatef(-x, -y, -z)

        # Render the scene
        place.render()

        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    main()
