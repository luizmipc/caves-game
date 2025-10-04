import json
import os


class Config:
    """Game configuration management."""

    CONFIG_FILE = "game_config.json"

    def __init__(self):
        """Initialize config with defaults."""
        self.maze_size = 5  # Default size (creates 11x11 grid)
        self.music_enabled = True  # Music on/off
        self.music_volume = 0.5  # Volume 0.0-1.0 (default 50%)
        self.load()

    def load(self):
        """Load config from file."""
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
        """Save config to file."""
        try:
            with open(self.CONFIG_FILE, 'w') as f:
                json.dump({
                    'maze_size': self.maze_size,
                    'music_enabled': self.music_enabled,
                    'music_volume': self.music_volume
                }, f, indent=2)
        except Exception as e:
            print(f"Could not save config: {e}")


# Global config instance
game_config = Config()
