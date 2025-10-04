import json
import os


class Config:
    """Game configuration management."""

    CONFIG_FILE = "game_config.json"

    def __init__(self):
        """Initialize config with defaults."""
        self.maze_size = 5  # Default size (creates 11x11 grid)
        self.load()

    def load(self):
        """Load config from file."""
        if os.path.exists(self.CONFIG_FILE):
            try:
                with open(self.CONFIG_FILE, 'r') as f:
                    data = json.load(f)
                    self.maze_size = data.get('maze_size', 5)
            except Exception as e:
                print(f"Could not load config: {e}")

    def save(self):
        """Save config to file."""
        try:
            with open(self.CONFIG_FILE, 'w') as f:
                json.dump({
                    'maze_size': self.maze_size
                }, f, indent=2)
        except Exception as e:
            print(f"Could not save config: {e}")


# Global config instance
game_config = Config()
