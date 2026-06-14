import subprocess
import sys
from typing import List, Optional
from binmanx.models import Binary


class Executor:
    def __init__(self, binary: Binary, args: Optional[List[str]] = None):
        self.binary = binary
        self.args = args if args is not None else []

    def execute(self) -> None:
        """Executes the binary"""
        if not self.binary.exists():
            print(f"Error: Binary for '{self.binary.alias}' does not exist in: {self.binary.path}")
            sys.exit(1)

        try:
            result = subprocess.run([self.binary.path] + self.args)

            sys.exit(result.returncode)

        except KeyboardInterrupt:
            sys.exit(130)