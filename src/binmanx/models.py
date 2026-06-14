from dataclasses import dataclass
from pathlib import Path

@dataclass
class Binary:
    alias: str
    path: str

    def exists(self) -> bool:
        """Checks if the binary exists"""
        return Path(self.path).exists()

    def to_dict(self) -> dict:
        """Turns the object to a dict to save on the JSON"""
        return {"alias": self.alias, "path": self.path}

    @classmethod
    def from_dict(cls, data: dict) -> 'Binary':
        """Makes anf instance of Binary from a dictionary"""
        return cls(alias=data["alias"], path = data["path"])