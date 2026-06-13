import json
from pathlib import Path
from typing import Dict
from binman.models import Binary

class ConfigManager:
    def __init__(self):
        self.config_dir = Path.home() / ".config" / "binman"
        self.config_file = self.config_dir / "config.json"

    def load_binaries(self) -> Dict[str, Binary]:
        """Reads the JSON and return a dictionary of Binary objects"""
        if not self.config_file.exists():
            return {}
        try:
            with open(self.config_file, "r", encoding="utf-8") as f:
                data = json.load(f)

                return {alias: Binary.from_dict(info) for alias, info in data.items()}
        except Exception:
            return {}

    def save_binaries(self, binaries: Dict[str, Binary]) -> None:
        self.config_dir.mkdir(parents=True, exist_ok=True)

        raw_data = {alias: binary.to_dict() for alias, binary in binaries.items()}

        with open(self.config_file, "w", encoding="utf-8") as f:
            json.dump(raw_data, f, indent=2)