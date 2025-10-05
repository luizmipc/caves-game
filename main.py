#!/usr/bin/env python3
"""
Dreamrooms - Um jogo de labirinto 3D com movimento em primeira pessoa.

Uma experiência de terror liminal inspirada por:
- Backrooms/Espaços Liminais
- Estética Dreamcore
- David Lynch (Twin Peaks, Estrada Perdida)
- Arte experimental de David Bowie

Controles:
- WASD: Movimentar
- Mouse: Olhar ao redor
- ESC: Sair
"""

# Importações da biblioteca padrão
import os

# Importações de terceiros
import pygame
from pygame.locals import *
from OpenGL.GL import *
from OpenGL.GLU import *
import numpy as np

# Importações dos módulos do jogo
from player.player import Player
from place.place import Place
from menu import Menu
from config_screen import ConfigScreen
from victory_screen import VictoryScreen
from config import game_config
from light.light import LightBall


# Caminho para o arquivo de música de fundo
SOUNDTRACK_PATH = "assets/audio/soundtrack.mp3"


def load_soundtrack():
    """
    Carrega e reproduz a trilha sonora de fundo em loop infinito.

    A trilha sonora toca durante o jogo para criar atmosfera.
    Se o arquivo não existir, o jogo continua sem música.
    """
    if os.path.exists(SOUNDTRACK_PATH):
        try:
            # Inicializa o mixer de áudio do pygame
            pygame.mixer.init()
            # Carrega o arquivo de música
            pygame.mixer.music.load(SOUNDTRACK_PATH)
            # Define o volume baseado na configuração
            pygame.mixer.music.set_volume(game_config.music_volume)
            # Toca em loop se a música estiver habilitada (-1 = loop infinito)
            if game_config.music_enabled:
                pygame.mixer.music.play(-1)
        except Exception as e:
            print(f"Não foi possível carregar a trilha sonora: {e}")


def update_music():
    """
    Atualiza a reprodução de música baseado nas configurações atuais.

    Chamado pela tela de configuração para aplicar mudanças sem reiniciar.
    Gerencia ajustes de volume e alternância de ligar/desligar.
    """
    # Atualiza o volume para corresponder à configuração atual
    pygame.mixer.music.set_volume(game_config.music_volume)

    # Inicia música se habilitada e não estiver tocando
    if game_config.music_enabled and not pygame.mixer.music.get_busy():
        pygame.mixer.music.play(-1)
    # Para música se desabilitada e estiver tocando
    elif not game_config.music_enabled and pygame.mixer.music.get_busy():
        pygame.mixer.music.stop()


def show_config(width, height):
    """
    Exibe a tela de configuração/ajustes.

    Args:
        width: Largura da janela em pixels
        height: Altura da janela em pixels

    Returns:
        str: Ação a tomar ('menu' para retornar ao menu, 'quit' para sair do jogo)
    """
    # Cria display 2D para interface de configuração
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption("Dreamrooms - Config")

    config_screen = ConfigScreen(width, height)
    clock = pygame.time.Clock()

    # Loop da tela de configuração
    while True:
        # Trata eventos (cliques do mouse, teclado, fechar janela)
        for event in pygame.event.get():
            if event.type == QUIT:
                return 'quit'

            # Deixa a tela de configuração tratar o evento
            action = config_screen.handle_event(event)
            if action == 'back':
                return 'menu'

        # Aplica mudanças de configuração de música em tempo real
        update_music()

        # Desenha interface da tela de configuração
        config_screen.render(screen)
        pygame.display.flip()
        clock.tick(60)  # 60 FPS


def show_victory(width, height):
    """Exibe a tela de vitória com créditos."""
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
    """Exibe o menu principal e retorna a escolha do usuário."""
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
    Inicializa as configurações de renderização OpenGL para visualização 3D.

    Configura a câmera em perspectiva e habilita teste de profundidade.

    Args:
        width: Largura da janela em pixels
        height: Altura da janela em pixels
    """
    # Habilita teste de profundidade para oclusão 3D adequada
    glEnable(GL_DEPTH_TEST)

    # Define o viewport para corresponder às dimensões da janela
    glViewport(0, 0, width, height)

    # Configura matriz de projeção em perspectiva
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    # FOV=45°, proporção de aspecto, perto=0.1, longe=1000 (estendido para ambiente externo)
    gluPerspective(45, width / height, 0.1, 1000.0)

    # Volta para matriz modelview para renderização
    glMatrixMode(GL_MODELVIEW)


def main():
    """
    Ponto de entrada principal para Dreamrooms.

    Fluxo do Jogo:
    1. Inicializa Pygame e áudio
    2. Exibe menu principal (Jogar/Configuração/Sair)
    3. Se Jogar for selecionado, gera labirinto e inicia loop do jogo
    4. Loop do jogo: Trata entrada, atualiza física/IA, renderiza cena 3D
    5. Vitória (alcançar saída) ou Game Over (capturado pelo inimigo)
    6. Sai para o sistema operacional
    """
    # ===== INICIALIZAÇÃO =====
    pygame.init()
    width, height = 800, 600

    # Carrega e reproduz trilha sonora de fundo
    load_soundtrack()

    # ===== LOOP DO MENU =====
    while True:
        action = show_menu(width, height)

        if action == 'quit':
            pygame.quit()
            return
        elif action == 'config':
            # Exibe tela de configurações
            config_action = show_config(width, height)
            if config_action == 'quit':
                pygame.quit()
                return
            # Se 'menu' for retornado, loop continua para mostrar menu novamente
        elif action == 'play':
            break  # Sai do loop do menu e inicia jogo

    # ===== CONFIGURAÇÃO DO JOGO =====

    # Cria contexto OpenGL com buffer duplo
    pygame.display.set_mode((width, height), DOUBLEBUF | OPENGL)
    pygame.display.set_caption("Dreamrooms - WASD to move, Mouse to look")

    # Esconde cursor do mouse e o trava na janela para controles FPS
    pygame.mouse.set_visible(False)
    pygame.event.set_grab(True)

    # Inicializa configurações OpenGL (perspectiva, teste de profundidade)
    setup_opengl(width, height)

    # Cria o mundo do jogo (labirinto, chão, paredes, inimigo)
    place = Place()

    # Gera jogador na posição inicial do labirinto
    if place.start_pos:
        player = Player(x=place.start_pos[0], y=place.start_pos[1], z=place.start_pos[2])
    else:
        # Posição de fallback se nenhuma posição inicial foi definida
        player = Player(x=0, y=1.7, z=5)

    # Cria a fonte de luz do jogador (spotlight tipo tocha)
    # Parâmetros: distância do jogador, deslocamento de altura, raio visual, alcance da luz
    light_ball = LightBall(distance=0.8, height_offset=-0.5, radius=0.15, light_range=15.0)

    # ===== VARIÁVEIS DO LOOP DO JOGO =====
    clock = pygame.time.Clock()  # Para controle de taxa de quadros
    running = True  # Controle do loop principal
    game_over = False  # Torna-se True quando inimigo captura jogador

    # Sistema de sobreposição de Vitória/Game Over
    credits_font = pygame.font.Font(None, 40)
    credits_lines = [
        "Credits:",
        "Game Developers:",
        "Leonardo Zordan Lima",
        "Luiz Marcelo Itapicuru Pereira Costa",
        "Matheus Soares Martins",
        "Thiago Crivaro Nunes"
    ]
    show_credits = False  # Alternador para sobreposição de vitória/game over
    credits_textures = []  # Texturas OpenGL para renderização de texto

    # ===== LOOP PRINCIPAL DO JOGO =====
    while running:
        # ===== TRATAMENTO DE EVENTOS =====
        for event in pygame.event.get():
            if event.type == QUIT:
                running = False

            elif event.type == KEYDOWN:
                if event.key == K_ESCAPE:
                    # ESC sempre funciona (mesmo durante game over)
                    running = False
                elif not game_over:
                    # Só processa entrada do jogador se jogo ainda está ativo
                    player.handle_key_down(event.key)

            elif event.type == KEYUP:
                if not game_over:
                    # Libera tecla (para movimento)
                    player.handle_key_up(event.key)

            elif event.type == MOUSEMOTION:
                if not game_over:
                    # Atualiza rotação da câmera baseado no movimento do mouse
                    player.handle_mouse_motion(event.rel[0], event.rel[1])

        # ===== FASE DE ATUALIZAÇÃO =====
        # Calcula tempo do quadro para física suave (alvo de 60 FPS)
        delta_time = clock.tick(60) / 1000.0  # Converte milissegundos para segundos

        # Atualiza movimento e física do jogador (só se jogo está ativo)
        if not game_over:
            player.update(delta_time, collision_check=place.framework.check_collision)

        # Obtém posição atual do jogador para IA e detecção de vitória
        x, y, z = player.get_position()

        # Atualiza IA do inimigo e verifica se jogador foi capturado
        player_caught = False
        if not game_over:
            player_caught = place.update(delta_time, x, z)

        # Verifica se inimigo capturou o jogador
        if player_caught and not show_credits:
            # Game Over - Toca áudio de morte e mostra tela de game over
            game_over = True  # Define flag de game over para congelar jogador
            death_audio_path = "assets/audio/death.mp3"
            if os.path.exists(death_audio_path):
                try:
                    pygame.mixer.music.load(death_audio_path)
                    pygame.mixer.music.play()
                except Exception as e:
                    print(f"Não foi possível reproduzir áudio de morte: {e}")

            # Gera textura de texto de game over
            show_credits = True  # Reutiliza sistema de sobreposição de créditos para game over
            credits_textures = []
            game_over_font = pygame.font.Font(None, 100)
            game_over_surf = game_over_font.render("GAME OVER", True, (255, 0, 0))

            # Converte para textura OpenGL
            texture_data = pygame.image.tostring(game_over_surf, "RGBA", True)
            tex_width = game_over_surf.get_width()
            tex_height = game_over_surf.get_height()

            texture_id = glGenTextures(1)
            glBindTexture(GL_TEXTURE_2D, texture_id)
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
            glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
            glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, tex_width, tex_height, 0, GL_RGBA, GL_UNSIGNED_BYTE, texture_data)

            credits_textures.append(('game_over', texture_id, tex_width, tex_height))

        # Verifica se jogador alcançou a saída (dispara vitória uma vez)
        if place.end_pos and not show_credits:
            exit_x, exit_y, exit_z = place.end_pos
            distance_to_exit = np.sqrt((x - exit_x)**2 + (z - exit_z)**2)
            if distance_to_exit < 2.0:  # Jogador está perto da saída
                # Vitória! Inicia música de encerramento e mostra sobreposição de créditos
                show_credits = True
                autro_path = "assets/audio/autro.mp3"
                if os.path.exists(autro_path):
                    try:
                        pygame.mixer.music.load(autro_path)
                        pygame.mixer.music.play(-1)
                    except Exception as e:
                        print(f"Não foi possível carregar música de encerramento: {e}")

                # Gera texturas de texto para créditos
                credits_textures = []
                title_font = pygame.font.Font(None, 60)
                title_surf = title_font.render("VICTORY!", True, (255, 215, 0))
                credits_textures.append(('title', title_surf))

                for line in credits_lines:
                    text_surf = credits_font.render(line, True, (200, 200, 200))
                    credits_textures.append(('line', text_surf))

                # Converte superfícies pygame para texturas OpenGL
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

        # Renderização
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glLoadIdentity()

        # Aplica transformações da câmera
        pitch, yaw = player.get_view_matrix_rotation()
        glRotatef(pitch, 1, 0, 0)
        glRotatef(yaw, 0, 1, 0)

        glTranslatef(-x, -y, -z)

        # Atualiza e renderiza bola de luz (configura iluminação e renderiza o orbe brilhante)
        # Se vitória, define luz ambiente máxima para revelar todo o labirinto
        if show_credits:
            glEnable(GL_LIGHTING)
            glEnable(GL_LIGHT0)
            glLightModelfv(GL_LIGHT_MODEL_AMBIENT, [1.0, 1.0, 1.0, 1.0])  # Luz ambiente máxima
            glLightfv(GL_LIGHT0, GL_DIFFUSE, [0.0, 0.0, 0.0, 1.0])  # Desabilita spotlight
            glEnable(GL_COLOR_MATERIAL)
            glColorMaterial(GL_FRONT_AND_BACK, GL_AMBIENT_AND_DIFFUSE)
        else:
            light_ball.update_and_render(x, y, z, yaw, pitch, collision_check=place.framework.check_collision)

        # Renderiza a cena
        place.render()

        # Renderiza inimigo (precisa ser renderizado separadamente para billboard)
        place.render_enemy(x, z)

        # Desabilita iluminação antes de renderizar interface
        if not show_credits:
            light_ball.disable_lighting()
        else:
            glDisable(GL_LIGHTING)
            glDisable(GL_LIGHT0)

        # Desenha sobreposição de créditos se vitória foi disparada (sobreposição 2D usando OpenGL)
        if show_credits and credits_textures:
            # Muda para projeção ortográfica 2D
            glMatrixMode(GL_PROJECTION)
            glPushMatrix()
            glLoadIdentity()
            glOrtho(0, width, height, 0, -1, 1)
            glMatrixMode(GL_MODELVIEW)
            glPushMatrix()
            glLoadIdentity()

            # Desabilita teste de profundidade para sobreposição 2D
            glDisable(GL_DEPTH_TEST)

            # Desenha caixa de fundo semi-transparente
            glEnable(GL_BLEND)
            glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
            glColor4f(0.0, 0.0, 0.0, 0.7)  # Preto semi-transparente
            glBegin(GL_QUADS)
            glVertex2f(0, 0)
            glVertex2f(width, 0)
            glVertex2f(width, height)
            glVertex2f(0, height)
            glEnd()

            # Habilita texturização
            glEnable(GL_TEXTURE_2D)
            glColor4f(1.0, 1.0, 1.0, 1.0)

            # Desenha texturas de texto
            y_pos = 70
            for text_type, texture_id, tex_width, tex_height in credits_textures:
                glBindTexture(GL_TEXTURE_2D, texture_id)

                x_pos = width // 2 - tex_width // 2  # Centraliza texto

                # Para game over, centraliza verticalmente também
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

            # Restaura projeção 3D
            glPopMatrix()
            glMatrixMode(GL_PROJECTION)
            glPopMatrix()
            glMatrixMode(GL_MODELVIEW)

            # Reabilita teste de profundidade
            glEnable(GL_DEPTH_TEST)

        pygame.display.flip()

    pygame.quit()


if __name__ == "__main__":
    main()
