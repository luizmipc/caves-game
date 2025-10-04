#!/usr/bin/env python3
"""
Dreamrooms - A 3D maze game with first-person player movement.

A liminal horror experience inspired by:
- Backrooms/Liminal Spaces
- Dreamcore aesthetics
- David Lynch (Twin Peaks, Lost Highway)
- David Bowie's experimental art

Controls:
- WASD: Move around
- Mouse: Look around
- ESC: Exit
"""

# Standard library imports
import os

# Third-party imports
import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
import numpy as np

# Game module imports
from player.player import Player
from place.place import Place
from menu import Menu
from config_screen import ConfigScreen
from victory_screen import VictoryScreen
from config import game_config
from light.light import LightBall


# Path to background music file
SOUNDTRACK_PATH = "assets/audio/soundtrack.mp3"


def load_soundtrack():
    """
    Load and play background soundtrack in an infinite loop.

    The soundtrack plays during gameplay to create atmosphere.
    If the file doesn't exist, the game continues without music.
    """
    if os.path.exists(SOUNDTRACK_PATH):
        try:
            # Initialize pygame's audio mixer
            pygame.mixer.init()
            # Load the music file
            pygame.mixer.music.load(SOUNDTRACK_PATH)
            # Set volume based on config
            pygame.mixer.music.set_volume(game_config.music_volume)
            # Play in loop if music is enabled (-1 = infinite loop)
            if game_config.music_enabled:
                pygame.mixer.music.play(-1)
        except Exception as e:
            print(f"Could not load soundtrack: {e}")


def update_music():
    """
    Update music playback based on current config settings.

    Called from config screen to apply changes without restarting.
    Handles volume adjustments and enable/disable toggling.
    """
    # Update volume to match current config
    pygame.mixer.music.set_volume(game_config.music_volume)

    # Start music if enabled and not already playing
    if game_config.music_enabled and not pygame.mixer.music.get_busy():
        pygame.mixer.music.play(-1)
    # Stop music if disabled and currently playing
    elif not game_config.music_enabled and pygame.mixer.music.get_busy():
        pygame.mixer.music.stop()


def show_config(width, height):
    """
    Display the configuration/settings screen.

    Args:
        width: Window width in pixels
        height: Window height in pixels

    Returns:
        str: Action to take ('menu' to return to menu, 'quit' to exit game)
    """
    # Create 2D display for config UI
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption("Dreamrooms - Config")

    config_screen = ConfigScreen(width, height)
    clock = pygame.time.Clock()

    # Config screen loop
    while True:
        # Handle events (mouse clicks, keyboard, window close)
        for event in pygame.event.get():
            if event.type == QUIT:
                return 'quit'

            # Let config screen handle the event
            action = config_screen.handle_event(event)
            if action == 'back':
                return 'menu'

        # Apply music setting changes in real-time
        update_music()

        # Draw config screen UI
        config_screen.render(screen)
        pygame.display.flip()
        clock.tick(60)  # 60 FPS


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
    """
    Initialize OpenGL rendering settings for 3D view.

    Sets up the perspective camera and enables depth testing.

    Args:
        width: Window width in pixels
        height: Window height in pixels
    """
    # Enable depth testing for proper 3D occlusion
    glEnable(GL_DEPTH_TEST)

    # Set the viewport to match window dimensions
    glViewport(0, 0, width, height)

    # Configure perspective projection matrix
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    # FOV=45°, aspect ratio, near=0.1, far=1000 (extended for outside environment)
    gluPerspective(45, width / height, 0.1, 1000.0)

    # Switch back to modelview matrix for rendering
    glMatrixMode(GL_MODELVIEW)


def main():
    """
    Main entry point for Dreamrooms.

    Game Flow:
    1. Initialize Pygame and audio
    2. Show main menu (Play/Config/Quit)
    3. If Play selected, generate maze and start game loop
    4. Game loop: Handle input, update physics/AI, render 3D scene
    5. Victory (reach exit) or Game Over (caught by enemy)
    6. Exit to operating system
    """
    # ===== INITIALIZATION =====
    pygame.init()
    width, height = 800, 600

    # Load and play background soundtrack
    load_soundtrack()

    # ===== MENU LOOP =====
    while True:
        action = show_menu(width, height)

        if action == 'quit':
            pygame.quit()
            return
        elif action == 'config':
            # Show settings screen
            config_action = show_config(width, height)
            if config_action == 'quit':
                pygame.quit()
                return
            # If 'menu' returned, loop continues to show menu again
        elif action == 'play':
            break  # Exit menu loop and start game

    # ===== GAME SETUP =====

    # Create OpenGL context with double buffering
    pygame.display.set_mode((width, height), DOUBLEBUF | OPENGL)
    pygame.display.set_caption("Dreamrooms - WASD to move, Mouse to look")

    # Hide mouse cursor and lock it to window for FPS controls
    pygame.mouse.set_visible(False)
    pygame.event.set_grab(True)

    # Initialize OpenGL settings (perspective, depth test)
    setup_opengl(width, height)

    # Create the game world (maze, floor, walls, enemy)
    place = Place()

    # Spawn player at maze start position
    if place.start_pos:
        player = Player(x=place.start_pos[0], y=place.start_pos[1], z=place.start_pos[2])
    else:
        # Fallback position if no start defined
        player = Player(x=0, y=1.7, z=5)

    # Create the player's light source (torch-like spotlight)
    # Parameters: distance from player, height offset, visual radius, light range
    light_ball = LightBall(distance=0.8, height_offset=-0.5, radius=0.15, light_range=15.0)

    # ===== GAME LOOP VARIABLES =====
    clock = pygame.time.Clock()  # For frame rate control
    running = True  # Main loop control
    game_over = False  # Becomes True when enemy catches player

    # Victory/Game Over overlay system
    credits_font = pygame.font.Font(None, 40)
    credits_lines = [
        "Credits:",
        "Game Developers:",
        "Leonardo Zordan Lima",
        "Luiz Marcelo Itapicuru Pereira Costa",
        "Matheus Soares Martins",
        "Thiago Crivaro Nunes"
    ]
    show_credits = False  # Toggle for victory/game over overlay
    credits_textures = []  # OpenGL textures for text rendering

    # ===== MAIN GAME LOOP =====
    while running:
        # ===== EVENT HANDLING =====
        for event in pygame.event.get():
            if event.type == QUIT:
                running = False

            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    # ESC always works (even during game over)
                    running = False
                elif not game_over:
                    # Only process player input if game is still active
                    player.handle_key_down(event.key)

            elif event.type == KEYUP:
                if not game_over:
                    # Release key (stop movement)
                    player.handle_key_up(event.key)

            elif event.type == MOUSEMOTION:
                if not game_over:
                    # Update camera rotation based on mouse movement
                    player.handle_mouse_motion(event.rel[0], event.rel[1])

        # ===== UPDATE PHASE =====
        # Calculate frame time for smooth physics (60 FPS target)
        delta_time = clock.tick(60) / 1000.0  # Convert milliseconds to seconds

        # Update player movement and physics (only if game is active)
        if not game_over:
            player.update(delta_time, collision_check=place.framework.check_collision)

        # Get current player position for AI and victory detection
        x, y, z = player.get_position()

        # Update enemy AI and check if player was caught
        player_caught = False
        if not game_over:
            player_caught = place.update(delta_time, x, z)

        # Check if enemy caught the player
        if player_caught and not show_credits:
            # Game Over - Play death audio and show game over screen
            game_over = True  # Set game over flag to freeze player
            death_audio_path = "assets/audio/death.mp3"
            if os.path.exists(death_audio_path):
                try:
                    pygame.mixer.music.load(death_audio_path)
                    pygame.mixer.music.play()
                except Exception as e:
                    print(f"Could not play death audio: {e}")

            # Generate game over text texture
            show_credits = True  # Reuse credits overlay system for game over
            credits_textures = []
            game_over_font = pygame.font.Font(None, 100)
            game_over_surf = game_over_font.render("GAME OVER", True, (255, 0, 0))

            # Convert to OpenGL texture
            texture_data = pygame.image.tostring(game_over_surf, "RGBA", True)
            tex_width = game_over_surf.get_width()
            tex_height = game_over_surf.get_height()

            texture_id = glGenTextures(1)
            glBindTexture(GL_TEXTURE_2D, texture_id)
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
            glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, tex_width, tex_height, 0, GL_RGBA, GL_UNSIGNED_BYTE, texture_data)

            credits_textures.append(('game_over', texture_id, tex_width, tex_height))

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
            glColor4f(0.0, 0.0, 0.0, 0.7)  # Semi-transparent black
            glBegin(GL_QUADS)
            glVertex2f(0, 0)
            glVertex2f(width, 0)
            glVertex2f(width, height)
            glVertex2f(0, height)
            glEnd()

            # Enable texturing
            glEnable(GL_TEXTURE_2D)
            glColor4f(1.0, 1.0, 1.0, 1.0)

            # Draw text textures
            y_pos = 70
            for text_type, texture_id, tex_width, tex_height in credits_textures:
                glBindTexture(GL_TEXTURE_2D, texture_id)

                x_pos = width // 2 - tex_width // 2  # Center text

                # For game over, center vertically too
                if text_type == 'game_over':
                    y_pos = height // 2 - tex_height // 2

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
