import json
import os


class Config:
    """Gerenciamento de configuração do jogo."""

    CONFIG_FILE = "game_config.json"

    def __init__(self):
        """Inicializa a configuração com valores padrão."""
        self.maze_size = 5  # Tamanho padrão (cria grid 11x11)
        self.music_enabled = True  # Música ligada/desligada
        self.music_volume = 0.5  # Volume 0.0-1.0 (padrão 50%)
        self.load()

    def load(self):
        """Carrega configuração do arquivo."""
        if os.path.exists(self.CONFIG_FILE):
            try:
                with open(self.CONFIG_FILE, 'r') as f:
                    data = json.load(f)
                    self.maze_size = data.get('maze_size', 5)
                    self.music_enabled = data.get('music_enabled', True)
                    self.music_volume = data.get('music_volume', 0.5)
            except Exception as e:
                print(f"Could not load config: {e}")

    def save(self):
        """Salva configuração no arquivo."""
        try:
            with open(self.CONFIG_FILE, 'w') as f:
                json.dump({
                    'maze_size': self.maze_size,
                    'music_enabled': self.music_enabled,
                    'music_volume': self.music_volume
                }, f, indent=2)
        except Exception as e:
            print(f"Could not save config: {e}")


# Instância global de configuração
game_config = Config()
