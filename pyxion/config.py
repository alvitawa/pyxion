from dataclasses import dataclass
from pathlib import Path
import toml
import sys

@dataclass
class Config:
    """Application configuration loaded from config.toml."""
    config_dir: Path
    precision: int = 4
    font_size: int = 20

    @classmethod
    def load(cls, config_dir: Path):
        """Load configuration from config.toml in config_dir."""
        config_path = config_dir / 'config.toml'
        data = {}
        if config_path.exists():
            try:
                data = toml.loads(config_path.read_text())
            except Exception as e:
                print(f"Failed to read config: {e}", file=sys.stderr)
        return cls(
            config_dir=config_dir,
            precision=int(data.get('precision', cls.precision)),
            font_size=int(data.get('font_size', cls.font_size)),
        )
